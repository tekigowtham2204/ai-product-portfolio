"""
Generate synthetic user event data for AI Agent Activation & Growth Funnel analysis.

Produces:
  - data/events.db   (SQLite database)
  - data/users.csv
  - data/events.csv

Cohort definitions
------------------
power_user  (30%) : completes all onboarding, runs agent multiple times, high retention
casual_user (40%) : partial onboarding, runs agent once, moderate retention
churned     (30%) : drops off early in onboarding, never activates
"""

import sqlite3
import random
import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

SEED = 42
N_USERS = 5000
random.seed(SEED)
np.random.seed(SEED)

# --------------------------------------------------------------------------- #
# Cohort weights and behavioural parameters
# --------------------------------------------------------------------------- #
COHORT_WEIGHTS = {"power_user": 0.30, "casual_user": 0.40, "churned": 0.30}

# P(completing each funnel step | previous step completed)
FUNNEL_PROBS = {
    "power_user": {
        "onboarding_step_1": 0.95,
        "onboarding_step_2": 0.90,
        "onboarding_step_3": 0.85,
        "first_agent_run":   0.90,
        "second_agent_run":  0.85,
        "retained_day7":     0.80,
        "retained_day30":    0.70,
    },
    "casual_user": {
        "onboarding_step_1": 0.80,
        "onboarding_step_2": 0.55,
        "onboarding_step_3": 0.40,
        "first_agent_run":   0.50,
        "second_agent_run":  0.30,
        "retained_day7":     0.35,
        "retained_day30":    0.15,
    },
    "churned": {
        "onboarding_step_1": 0.50,
        "onboarding_step_2": 0.20,
        "onboarding_step_3": 0.08,
        "first_agent_run":   0.10,
        "second_agent_run":  0.04,
        "retained_day7":     0.05,
        "retained_day30":    0.02,
    },
}

# Median minutes after signup for each event (for casual users; scaled for others)
EVENT_DELAY_MINUTES = {
    "onboarding_step_1": 2,
    "onboarding_step_2": 8,
    "onboarding_step_3": 20,
    "first_agent_run":   60,
    "second_agent_run":  180,
    "retained_day7":     7 * 24 * 60,
    "retained_day30":    30 * 24 * 60,
}

SPEED_FACTOR = {"power_user": 0.5, "casual_user": 1.0, "churned": 1.5}

# Signup spread: last 12 weeks
START_DATE = datetime(2024, 1, 1)
END_DATE   = datetime(2024, 3, 24)

FUNNEL_STEPS = [
    "signed_up",
    "onboarding_step_1",
    "onboarding_step_2",
    "onboarding_step_3",
    "first_agent_run",
    "second_agent_run",
    "retained_day7",
    "retained_day30",
]

# --------------------------------------------------------------------------- #
# Generate users
# --------------------------------------------------------------------------- #
cohorts = random.choices(
    list(COHORT_WEIGHTS.keys()),
    weights=list(COHORT_WEIGHTS.values()),
    k=N_USERS,
)

# Signup timestamps uniformly distributed over the window
total_seconds = int((END_DATE - START_DATE).total_seconds())
signup_offsets = np.random.randint(0, total_seconds, size=N_USERS)
signup_times   = [START_DATE + timedelta(seconds=int(s)) for s in signup_offsets]

# Acquisition channel
channels = random.choices(
    ["organic_search", "paid_social", "referral", "direct", "email_campaign"],
    weights=[0.30, 0.25, 0.20, 0.15, 0.10],
    k=N_USERS,
)

users = pd.DataFrame({
    "user_id":    [f"u{i:05d}" for i in range(N_USERS)],
    "cohort":     cohorts,
    "signup_at":  signup_times,
    "channel":    channels,
    "signup_week": [t.strftime("%Y-W%W") for t in signup_times],
})

# --------------------------------------------------------------------------- #
# Generate events
# --------------------------------------------------------------------------- #
rows = []

for _, user in users.iterrows():
    uid     = user["user_id"]
    cohort  = user["cohort"]
    t       = user["signup_at"]
    probs   = FUNNEL_PROBS[cohort]
    speed   = SPEED_FACTOR[cohort]

    # signed_up is always recorded
    rows.append({"user_id": uid, "event": "signed_up", "occurred_at": t, "cohort": cohort})

    for step in FUNNEL_STEPS[1:]:
        if random.random() > probs[step]:
            break   # user dropped off; no further steps
        delay_mins = EVENT_DELAY_MINUTES[step] * speed
        # add some noise (log-normal)
        actual_delay = max(1, np.random.lognormal(np.log(delay_mins), 0.4))
        t = t + timedelta(minutes=actual_delay)
        rows.append({"user_id": uid, "event": step, "occurred_at": t, "cohort": cohort})

events = pd.DataFrame(rows)
events["occurred_at"] = pd.to_datetime(events["occurred_at"])

# --------------------------------------------------------------------------- #
# Persist to CSV
# --------------------------------------------------------------------------- #
out_dir = os.path.dirname(os.path.abspath(__file__))
users_csv  = os.path.join(out_dir, "users.csv")
events_csv = os.path.join(out_dir, "events.csv")
db_path    = os.path.join(out_dir, "events.db")

users.to_csv(users_csv, index=False)
events.to_csv(events_csv, index=False)

# --------------------------------------------------------------------------- #
# Persist to SQLite
# --------------------------------------------------------------------------- #
if os.path.exists(db_path):
    os.remove(db_path)

con = sqlite3.connect(db_path)

users[["user_id", "cohort", "signup_at", "channel", "signup_week"]].to_sql(
    "users", con, if_exists="replace", index=False
)

events[["user_id", "event", "occurred_at", "cohort"]].to_sql(
    "events", con, if_exists="replace", index=False
)

# Helpful indexes
con.execute("CREATE INDEX idx_events_user  ON events(user_id)")
con.execute("CREATE INDEX idx_events_event ON events(event)")
con.commit()
con.close()

print(f"Generated {len(users)} users and {len(events)} events.")
print(f"  CSV  -> {users_csv}")
print(f"  CSV  -> {events_csv}")
print(f"  DB   -> {db_path}")

cohort_counts = users["cohort"].value_counts()
print("\nCohort distribution:")
for c, n in cohort_counts.items():
    print(f"  {c:<15} {n:>5} ({n/N_USERS:.1%})")
