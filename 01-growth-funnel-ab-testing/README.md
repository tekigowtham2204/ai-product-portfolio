# AI Agent Activation & Growth Funnel Optimization

**AI Product Analyst Portfolio Project**

An end-to-end product analytics case study covering funnel analysis, cohort retention, A/B test design, and growth recommendations for a hypothetical AI agent SaaS product.

---

## Project Overview

This project answers a common growth question:

> *Why do most users who sign up never run their first AI agent — and what should we do about it?*

Using synthetic data modelling 5,000 users across three behavioural cohorts, the analysis traces the full user journey from sign-up through onboarding, activation, and 30-day retention. It culminates in a statistically-grounded A/B test proposal and an executive growth brief.

### Key Findings

| Finding | Detail |
|---------|--------|
| **Activation bottleneck** | Only ~38% of signups complete `first_agent_run`; the primary funnel leak |
| **Biggest single drop** | Onboarding Step 2 → Step 3 loses ~22% of remaining users |
| **Activation predicts retention** | Users who activate retain at 60%+ on Day 7; non-activators churn immediately |
| **Casual users are the prize** | 40% of signups; activation rate improvable by 10 pp with onboarding simplification |
| **Paid social quality problem** | Paid social cohort shows worst retention quality index vs. referral/organic |
| **A/B test ready** | Streamlined onboarding needs only ~2,000 users per arm to detect a 5 pp lift |

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Data generation, analysis |
| pandas | Data manipulation and SQL result processing |
| SQLite (built-in) | Persistent event store, SQL query execution |
| matplotlib + seaborn | Publication-quality charts |
| scipy.stats | Sample size and power calculations |
| Jupyter Notebook | Interactive analysis and presentation |

---

## Repository Structure

```
01-growth-funnel-ab-testing/
├── README.md                  ← This file
├── analysis.ipynb             ← Main Jupyter notebook (run this)
├── growth_brief.md            ← Executive-ready 3-page growth brief
├── funnel_chart.png           ← Generated: funnel drop-off chart
├── retention_heatmap.png      ← Generated: weekly cohort heatmap
├── retention_curves.png       ← Generated: segment retention curves
├── power_curve.png            ← Generated: A/B test power curve
├── data/
│   ├── generate_data.py       ← Synthetic data generator
│   ├── events.db              ← Generated: SQLite database
│   ├── users.csv              ← Generated: user records
│   └── events.csv             ← Generated: event log
└── sql/
    └── cohort_analysis.sql    ← 5 standalone SQL queries with CTEs
```

---

## How to Run

### 1. Install dependencies

```bash
pip install pandas matplotlib seaborn scipy jupyter numpy
```

### 2. Run the notebook

```bash
cd 01-growth-funnel-ab-testing
jupyter notebook analysis.ipynb
```

The notebook will:
1. Call `data/generate_data.py` to create the SQLite database and CSV files
2. Execute all SQL analysis queries via `sqlite3`
3. Render all four charts inline and save them as PNG files
4. Display the full A/B test design with sample size and power curve

### 3. Run data generation standalone (optional)

```bash
python data/generate_data.py
```

### 4. Run SQL queries directly (optional)

```bash
sqlite3 data/events.db < sql/cohort_analysis.sql
```

---

## Visual Outputs

### Chart 1: Activation Funnel Drop-off
A horizontal bar chart showing the number of users at each funnel step (signed_up → retained_day30), annotated with cumulative conversion percentages and step-over-step drop percentages. Colour gradient shifts from green (top of funnel) to red (deep funnel) to visually reinforce attrition.

### Chart 2: Weekly Cohort Retention Heatmap
A seaborn heatmap where rows are signup weeks (12 weeks of data) and columns are Day-7 and Day-30 retention rates. Colour intensity (YlGn scale) makes it immediately obvious which cohorts retained best and whether there are any week-over-week regressions that might indicate onboarding changes or seasonal effects.

### Chart 3: Retention Curves by User Segment
A line chart showing three retention curves (Power User, Casual User, Churned) from Day 0 (100%) through Day 7 and Day 30. The gap between power users and churned users is shaded to illustrate the addressable retention opportunity. Final Day-30 values are annotated directly on the chart.

### Chart 4: A/B Test Power Curve
A multi-line chart showing statistical power (y-axis) as a function of minimum detectable effect size (x-axis) for four different sample sizes per arm. The recommended sample size (for 80% power at 5 pp MDE) is highlighted in blue. A horizontal dashed line marks the 80% power threshold, and a vertical dotted line marks the target MDE.

---

## SQL Queries Summary (`sql/cohort_analysis.sql`)

1. **Funnel drop-off by step** — step-over-step and cumulative conversion using CTEs and `LAG()`
2. **Weekly cohort retention matrix** — `GROUP BY signup_week` with conditional aggregation for D7/D30
3. **Retention by acquisition channel** — channel quality ranking including a retention quality index (D30/D7)
4. **High drop-off segments** — `cohort × channel` combinations with stall-step identification using window functions
5. **Time-to-activation distribution** — `julianday()` arithmetic to compute hours from sign-up to first agent run, with approximate median

---

## Synthetic Data Design

The data generator creates three realistic user cohorts with distinct behavioural profiles:

| Cohort | Share | Onboarding Completion | Activation Rate | Day-30 Retention |
|--------|:-----:|:---------------------:|:---------------:|:----------------:|
| Power User | 30% | ~85% | ~90% | ~70% |
| Casual User | 40% | ~40% | ~50% | ~15% |
| Churned | 30% | ~8% | ~10% | ~2% |

Event timestamps use log-normal noise around realistic median delays (e.g., median 2 min to Step 1, 60 min to first agent run), making the data plausible for time-based analyses. Users are spread across 12 signup weeks and 5 acquisition channels to enable cohort and channel-level cuts.

---

## Growth Brief

See [`growth_brief.md`](growth_brief.md) for the full executive-ready document including:
- Executive summary with top 3 recommendations
- Funnel analysis with annotated drop-off table
- Three high-priority user segments with root-cause hypotheses
- A/B test proposal with full statistical design (α, power, MDE, sample size, decision rules)
- 90-day intervention roadmap with estimated impact

---

*All data in this project is synthetic and generated for portfolio demonstration purposes.*
