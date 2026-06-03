"""
generate_transcripts.py
Generates 200 synthetic AI voice agent call transcripts with realistic
conversation patterns and deliberate failure modes injected.
"""

import json
import random
import math
from datetime import datetime, timedelta

random.seed(42)

# ── Constants ──────────────────────────────────────────────────────────────────

CATEGORIES = [
    "billing_dispute",
    "technical_support",
    "account_access",
    "product_inquiry",
    "cancellation_request",
]

OUTCOMES = ["resolved", "escalated", "abandoned"]

AGENT_IDS = [f"AGT-{i:03d}" for i in range(1, 11)]
CUSTOMER_IDS = [f"CUST-{i:05d}" for i in range(10001, 10201)]

BASE_DATE = datetime(2024, 1, 1, 8, 0, 0)

# ── Conversation Templates ─────────────────────────────────────────────────────

OPENING_AGENT = [
    "Thank you for calling support. My name is Alex. How can I assist you today?",
    "Hello! You've reached customer support. How may I help you?",
    "Good day! This is the support line. What can I do for you today?",
    "Welcome to support. I'm here to help. What's the issue you're experiencing?",
]

OPENING_CUSTOMER = {
    "billing_dispute": [
        "I was charged twice on my last bill and I need this fixed immediately.",
        "There's an incorrect charge on my account. I never authorized this payment.",
        "My bill is way higher than it should be. Can you explain these charges?",
        "I was promised a discount that never showed up on my invoice.",
        "I cancelled my subscription last month but you still charged me.",
    ],
    "technical_support": [
        "My device isn't connecting to the network and I've tried everything.",
        "The app keeps crashing whenever I try to open it. This is unacceptable.",
        "I'm getting error code 502 every time I try to log in.",
        "My service has been down for three hours. What's going on?",
        "I updated the firmware and now nothing works properly.",
    ],
    "account_access": [
        "I can't log into my account. I've reset my password twice already.",
        "My account appears to be locked and I don't know why.",
        "I'm getting a two-factor authentication error even with the correct code.",
        "My account was suspended but I haven't violated any terms.",
        "I lost access to my email so now I can't verify my identity.",
    ],
    "product_inquiry": [
        "I want to know if your premium plan includes API access.",
        "What's the difference between the business and enterprise tiers?",
        "Can I use your service in multiple countries simultaneously?",
        "I need to know your data retention and privacy policies before signing up.",
        "Does your product integrate with Salesforce and HubSpot?",
    ],
    "cancellation_request": [
        "I need to cancel my subscription effective immediately.",
        "I want to cancel. The service isn't meeting my expectations.",
        "Please cancel my account. I'm switching to a competitor.",
        "I've been meaning to cancel for a while. Can you process that now?",
        "I need to downgrade or cancel. The cost is too high for what I get.",
    ],
}

AGENT_RESPONSES = {
    "billing_dispute": [
        "I understand your frustration. Let me pull up your account and review the charges.",
        "I can see your billing history here. Let me identify that discrepancy for you.",
        "I'm reviewing your payment records now. Can you confirm the charge amount?",
        "I've located the duplicate charge. I'll initiate a refund right away.",
        "I can apply that discount retroactively. It should appear within 3-5 business days.",
    ],
    "technical_support": [
        "Let me run a diagnostic on your account to identify the issue.",
        "Can you try clearing your cache and restarting the application?",
        "I'm checking our system status. There's a known outage in your region.",
        "Let me escalate this to our technical team for a deeper investigation.",
        "Have you tried uninstalling and reinstalling the latest version?",
    ],
    "account_access": [
        "Let me verify your identity before we make any changes to the account.",
        "I can see your account has been flagged for suspicious activity.",
        "I'll manually reset your access. You should receive an email within 10 minutes.",
        "Let me bypass the two-factor step for this session and reset your authenticator.",
        "I'm restoring your account access now. Please try logging in again.",
    ],
    "product_inquiry": [
        "Great question. Let me pull up the full feature comparison for you.",
        "Yes, API access is included in all plans above the starter tier.",
        "Our enterprise plan supports multi-region deployments with data residency options.",
        "I can send you our full privacy policy and data processing agreement.",
        "We have native integrations with both Salesforce and HubSpot in the Pro plan.",
    ],
    "cancellation_request": [
        "I'm sorry to hear that. Before I process the cancellation, may I ask what's driving this decision?",
        "I understand. Let me check if there are any retention offers available for your account.",
        "I can process that cancellation. Your service will remain active until the end of the billing cycle.",
        "I'd hate to lose you as a customer. Can I offer you a 30% discount to stay?",
        "I've initiated the cancellation. You'll receive a confirmation email shortly.",
    ],
}

CUSTOMER_FOLLOWUP = {
    "billing_dispute": [
        "How long will the refund take? I need this resolved today.",
        "Okay, but why did it happen in the first place?",
        "That's still not right. The amount is different from what I see.",
        "Fine. As long as I get my money back.",
        "This is the third time this has happened. I'm losing patience.",
    ],
    "technical_support": [
        "I already tried that. It didn't work.",
        "How long will the outage last? I need this for work.",
        "So there's nothing you can do right now?",
        "Okay, I'll try that. But if it doesn't work I'm calling back.",
        "This is really affecting my productivity. Can I get compensation?",
    ],
    "account_access": [
        "I've been waiting 20 minutes already. This is taking too long.",
        "I'm not getting the email. Can you resend it?",
        "Why was my account flagged? I haven't done anything wrong.",
        "Okay, I'll try again. But this is very inconvenient.",
        "What do I need to do to make sure this doesn't happen again?",
    ],
    "product_inquiry": [
        "That sounds good but I need to confirm the pricing too.",
        "Is there a free trial available before I commit?",
        "Can I speak to a sales representative for more details?",
        "What happens to my data if I decide to cancel later?",
        "Okay, I think I have enough information. Thank you.",
    ],
    "cancellation_request": [
        "I appreciate the offer but I've already made my decision.",
        "What happens to all my data after cancellation?",
        "Will I get a prorated refund for the remaining days?",
        "Fine, I'll think about the discount offer.",
        "Can you confirm the exact cancellation date?",
    ],
}

AGENT_CLOSING = [
    "Is there anything else I can help you with today?",
    "I've noted everything on your account. Is there anything else?",
    "Thank you for your patience. Is there anything else I can assist with?",
    "I've resolved that for you. Do you have any other questions?",
    "Your issue has been addressed. Is there anything else?",
]

CUSTOMER_CLOSING = [
    "No, that's all. Thank you.",
    "That's everything. Goodbye.",
    "Okay, thanks. I appreciate the help.",
    "No, I'm good. Have a nice day.",
    "That's all I needed. Thanks.",
]

# Failure mode dialogues
AGENT_LOOP_RESPONSES = [
    "I understand your concern. Let me look into that for you.",
    "I understand your concern. Let me look into that for you.",
    "I understand your concern. Let me look into that for you.",
]

WRONG_INFO_RESPONSES = [
    "Our refund policy allows up to 90 days from purchase.",  # wrong - should be 30
    "Yes, that feature is available on all plans including the free tier.",  # wrong
    "Your data will be deleted immediately upon cancellation.",  # misleading
]

EXCESSIVE_LATENCY_MESSAGES = [
    "Please hold while I check that for you... this may take a moment.",
    "I'm still looking into this. Thank you for your patience...",
    "Please bear with me, the system is loading your records...",
    "Just a few more moments while I access that information...",
]

SENTIMENT_MISMATCH_RESPONSES = [
    "That's great! I'm so glad we could help you today.",  # agent upbeat when customer is angry
    "Wonderful! Have a fantastic day!",  # inappropriate positive close after complaint
    "Excellent! Everything looks perfect on our end.",  # dismissive of real issue
]

# ── Transcript Builder ─────────────────────────────────────────────────────────

def build_transcript(call_id, category, outcome, inject_failure=None):
    """Build a realistic multi-turn transcript with optional failure injection."""
    turns = []
    offset = 0.0

    def add_turn(speaker, text, extra_pause=0):
        nonlocal offset
        offset += random.uniform(0.5, 2.0) + extra_pause
        turns.append({
            "speaker": speaker,
            "text": text,
            "timestamp_offset": round(offset, 2),
        })
        # Approximate words-per-second pause for next turn
        word_count = len(text.split())
        offset += word_count * 0.35  # ~170 wpm

    # Opening exchange
    add_turn("agent", random.choice(OPENING_AGENT))
    add_turn("customer", random.choice(OPENING_CUSTOMER[category]))

    # ── Inject failure modes ──
    if inject_failure == "agent_loop":
        for msg in AGENT_LOOP_RESPONSES:
            add_turn("agent", msg)
            add_turn("customer", "You already said that. Can you actually help me?")
        add_turn("agent", "Let me transfer you to a specialist who can better assist.")

    elif inject_failure == "wrong_information":
        add_turn("agent", random.choice(WRONG_INFO_RESPONSES))
        add_turn("customer", "Are you sure about that? That doesn't match what I read online.")
        add_turn("agent", random.choice(AGENT_RESPONSES[category]))
        add_turn("customer", random.choice(CUSTOMER_FOLLOWUP[category]))

    elif inject_failure == "excessive_latency":
        add_turn("agent", random.choice(AGENT_RESPONSES[category]))
        for msg in EXCESSIVE_LATENCY_MESSAGES[:3]:
            add_turn("agent", msg, extra_pause=8.0)
        add_turn("customer", "Are you still there? This is taking forever.")
        add_turn("agent", "Yes, I apologize for the wait. I'm still processing your request.")

    elif inject_failure == "sentiment_mismatch":
        add_turn("agent", random.choice(AGENT_RESPONSES[category]))
        add_turn("customer", "This is absolutely unacceptable. I'm extremely upset about this.")
        add_turn("agent", random.choice(SENTIMENT_MISMATCH_RESPONSES))
        add_turn("customer", "Did you even hear what I just said? I'm not happy at all.")

    elif inject_failure == "loop_detection_failure":
        # Agent fails to detect that customer is stuck in a loop asking the same thing
        repeated = random.choice(CUSTOMER_FOLLOWUP[category])
        add_turn("agent", random.choice(AGENT_RESPONSES[category]))
        add_turn("customer", repeated)
        add_turn("agent", random.choice(AGENT_RESPONSES[category]))
        add_turn("customer", repeated)
        add_turn("agent", random.choice(AGENT_RESPONSES[category]))
        add_turn("customer", repeated)
        add_turn("agent", "I believe I've answered that question. Is there anything else?")

    else:
        # Normal helpful exchange
        add_turn("agent", random.choice(AGENT_RESPONSES[category]))
        add_turn("customer", random.choice(CUSTOMER_FOLLOWUP[category]))

        # Mid-call elaboration
        if random.random() > 0.4:
            add_turn("agent", random.choice(AGENT_RESPONSES[category]))
            add_turn("customer", random.choice(CUSTOMER_FOLLOWUP[category]))

    # Outcome-specific closing
    if outcome == "resolved":
        add_turn("agent", random.choice(AGENT_CLOSING))
        add_turn("customer", random.choice(CUSTOMER_CLOSING))

    elif outcome == "escalated":
        add_turn("agent", "I'm going to connect you with a senior specialist who can better handle this.")
        add_turn("customer", "Finally. I've been waiting for a real solution.")
        add_turn("agent", "Please hold while I transfer you. Thank you for your patience.")

    elif outcome == "abandoned":
        add_turn("customer", "You know what, forget it. This is pointless.")
        # Call ends without proper close

    duration = round(offset + random.uniform(5, 20))
    return turns, duration


def generate_call(index, customer_id):
    """Generate a single call record."""
    category = random.choices(
        CATEGORIES,
        weights=[25, 30, 20, 15, 10],
        k=1,
    )[0]

    # Outcome probabilities vary by category
    outcome_weights = {
        "billing_dispute":      [55, 30, 15],
        "technical_support":    [45, 35, 20],
        "account_access":       [50, 35, 15],
        "product_inquiry":      [75, 10, 15],
        "cancellation_request": [40, 45, 15],
    }
    outcome = random.choices(OUTCOMES, weights=outcome_weights[category], k=1)[0]

    # Inject failures into ~30% of calls
    failure_modes = [
        "agent_loop",
        "wrong_information",
        "excessive_latency",
        "sentiment_mismatch",
        "loop_detection_failure",
        None,
    ]
    failure_weights = [5, 6, 6, 6, 5, 72]
    inject_failure = random.choices(failure_modes, weights=failure_weights, k=1)[0]

    agent_id = random.choice(AGENT_IDS)
    timestamp = BASE_DATE + timedelta(
        days=random.randint(0, 89),
        hours=random.randint(0, 11),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )

    turns, duration = build_transcript(index, category, outcome, inject_failure)

    # Add injected_failure_mode for ground truth labeling
    record = {
        "call_id": f"CALL-{index:05d}",
        "agent_id": agent_id,
        "customer_id": customer_id,
        "timestamp": timestamp.isoformat(),
        "duration_seconds": duration,
        "call_category": category,
        "outcome": outcome,
        "injected_failure_mode": inject_failure,  # ground truth for analysis
        "transcript": turns,
    }
    return record


def main():
    random.seed(42)
    calls = []
    customer_pool = random.sample(CUSTOMER_IDS, len(CUSTOMER_IDS))

    for i in range(1, 201):
        customer_id = customer_pool[(i - 1) % len(customer_pool)]
        call = generate_call(i, customer_id)
        calls.append(call)

    output_path = "data/transcripts.json"
    with open(output_path, "w") as f:
        json.dump(calls, f, indent=2)

    print(f"Generated {len(calls)} transcripts → {output_path}")

    # Summary stats
    from collections import Counter
    cats = Counter(c["call_category"] for c in calls)
    outs = Counter(c["outcome"] for c in calls)
    fails = Counter(c["injected_failure_mode"] for c in calls if c["injected_failure_mode"])

    print("\nCategory distribution:")
    for k, v in cats.most_common():
        print(f"  {k}: {v}")

    print("\nOutcome distribution:")
    for k, v in outs.most_common():
        print(f"  {k}: {v}")

    print("\nInjected failure modes:")
    for k, v in fails.most_common():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
