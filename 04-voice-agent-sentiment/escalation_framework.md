# Escalation Framework for AI Voice Agents

**Document type:** Operational Framework  
**Applies to:** AI Voice Agent deployments in customer support  
**Version:** 1.0

---

## 1. Purpose

This document defines the escalation framework for AI voice agents handling inbound customer support calls. It specifies confidence score thresholds, trigger logic, human handoff protocol, and the metrics used to evaluate escalation quality over time.

The goal is to maximize automation coverage while protecting customers from poor outcomes — specifically: unresolved issues, incorrect information, and emotional harm from tone-deaf AI responses.

---

## 2. Confidence Score Model

Every call is evaluated in real-time across two dimensions:

### 2.1 Resolution Confidence Score (0–1)
Estimates how likely the AI agent has correctly resolved the customer's issue.

**Inputs:**
- Presence of resolution-confirming language ("your refund has been initiated," "your access is restored")
- Customer acknowledgment of resolution ("okay, thanks," "that's all I needed")
- Issue category match confidence (did the AI correctly classify the problem?)
- Absence of escalation-indicator phrases ("this is unacceptable," "I want to speak to a human")

**Computation:** Weighted keyword scoring normalized to [0, 1]. Values below 0.40 indicate the agent has likely failed to resolve the issue.

### 2.2 Customer Sentiment Score (−1 to +1)
Tracks emotional valence of the customer across the call.

**Inputs:**
- Negative emotion keywords: "frustrated," "unacceptable," "this is ridiculous"
- Positive emotion keywords: "thank you," "appreciate," "that works"
- Outcome-adjusted: resolved calls receive a +0.2 adjustment; abandoned calls receive −0.4

**Computation:** (positive_hits − 1.5 × negative_hits) / normalizer + outcome_adjustment, clipped to [−1, 1].

---

## 3. Escalation Trigger Logic

### 3.1 Primary Rule

Escalate if **either** condition is met:

```
resolution_confidence < 0.40
OR
customer_sentiment < 0.10
```

This combined rule was selected based on threshold sweep analysis across 200 calls:
- At t = 0.40, true positive rate = ~0.72 with false positive rate = ~0.22
- Moving from t = 0.30 to t = 0.40 reduces false-positive escalations by approximately 35%
- F1 score peaks in the 0.35–0.45 range

### 3.2 Secondary Hard Triggers

These trigger escalation regardless of score values:

| Trigger | Condition | Rationale |
|---|---|---|
| **Agent Loop** | Same agent utterance repeated 3+ times | Agent is stuck; further AI handling will worsen customer experience |
| **Explicit Human Request** | Customer says "speak to a human" or "get me a manager" | Mandatory; never suppress |
| **High-Risk Category + Negative Sentiment** | `cancellation_request` + `sentiment < 0.0` | Churn risk; human has authority to offer better retention |
| **Excessive Duration** | Call duration > mean + 2σ for its category | Complex issue exceeding AI capability; prevent abandonment |
| **Compliance Flag** | Wrong information detected via keyword rules | Regulatory risk; incorrect policy statements require human correction |

### 3.3 Confidence Score Threshold Selection Rationale

| Threshold | TPR | FPR | False Positives | Recommendation |
|---|---|---|---|---|
| 0.20 | High | Very high | Too many unnecessary escalations | Not recommended |
| 0.30 | ~0.82 | ~0.38 | Overescalates by ~35% | Fallback for high-stakes deployments |
| **0.40** | **~0.72** | **~0.22** | **Optimal balance** | **Recommended default** |
| 0.50 | ~0.61 | ~0.14 | May miss true escalations | Use only with high agent confidence baseline |
| 0.60+ | Low | Low | Under-escalation risk | Not recommended for most deployments |

**Recommended threshold: 0.40** for general support. Adjust downward to 0.30 for:
- Financial or billing disputes above a defined dollar amount
- Healthcare or safety-related inquiries
- Customers with prior escalation history

---

## 4. Human Handoff Protocol

### 4.1 Warm Transfer (Preferred)

1. AI agent informs customer: *"I'd like to connect you with a specialist who can better assist with this."*
2. AI agent sends structured handoff packet to human agent (see 4.3)
3. Human agent receives call with full context — no re-authentication required
4. Human agent reviews handoff packet before speaking

### 4.2 Async Review (for post-call flags)

When escalation is detected after call completion (e.g., sentiment scoring runs post-call):

1. Call is flagged in QA queue with escalation reason
2. Human reviewer contacts customer proactively within 1 business day
3. Resolution confirmed and logged

### 4.3 Handoff Packet Contents

The following structured data is passed to the human agent at escalation:

```json
{
  "call_id": "CALL-00042",
  "escalation_reason": ["low_resolution_confidence", "agent_loop"],
  "customer_sentiment": -0.42,
  "resolution_confidence": 0.31,
  "call_category": "billing_dispute",
  "main_issue": "Customer was charged twice in December billing cycle",
  "ai_actions_taken": ["looked up account", "initiated refund investigation"],
  "failure_flags": ["agent_loop", "incomplete_resolution"],
  "suggested_resolution": "Verify double-charge in billing system; issue refund if confirmed",
  "priority": "high"
}
```

---

## 5. Metrics to Track

### 5.1 Escalation Quality Metrics (measure weekly)

| Metric | Formula | Target |
|---|---|---|
| **Escalation Rate** | escalated_calls / total_calls | < 30% |
| **Unnecessary Escalation Rate** | false_positive_escalations / total_escalations | < 20% |
| **Missed Escalation Rate** | false_negative_escalations / true_escalations | < 10% |
| **Human Resolution Rate** | human_resolved / human_escalated | > 90% |
| **Escalation-to-Resolution Time** | avg time from escalation trigger to resolution | < 8 minutes |

### 5.2 Threshold Drift Monitoring

Re-run threshold sweep monthly as:
- Agent model updates may shift confidence score distributions
- Seasonal call patterns shift sentiment baselines (e.g., billing cycles, product launches)
- False positive rate creep above 25% should trigger immediate threshold review

### 5.3 Human Reviewer Feedback Loop

Human agents review escalated calls and tag:
- Was the escalation justified? (yes / no / borderline)
- What was the root cause? (AI error / customer preference / genuine complexity)
- Was the handoff packet accurate?

This feedback trains future threshold calibration and improves the sentiment model.

---

## 6. Governance

- Escalation threshold changes require sign-off from both Product and Support Operations
- Any change to the primary rule (Section 3.1) must be A/B tested for ≥2 weeks before full rollout
- Compliance-flagged escalations must be logged in the audit trail with timestamp and operator ID
- Customer-requested human handoffs (Section 3.2) are never blocked under any threshold configuration
