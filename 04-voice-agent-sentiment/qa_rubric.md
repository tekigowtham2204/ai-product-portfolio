# QA Call Scoring Rubric — AI Voice Agent

**Document type:** Quality Assurance Rubric  
**Applies to:** AI voice agent calls and human-reviewed escalations  
**Scoring range:** 0–100 (5 dimensions × 0–20 each)

---

## Overview

This rubric provides a standardized scoring framework for evaluating AI voice agent call quality. It is used for:
- Automated QA scoring via the analytics pipeline
- Human reviewer calibration when reviewing flagged calls
- Agent model performance benchmarking
- Identifying training data candidates for model improvement

A call scoring below **70/100** should be reviewed by a QA analyst. Calls below **50/100** require immediate remediation review and may require proactive customer follow-up.

---

## Dimension 1: Accuracy (0–20)

**Definition:** The agent provided factually correct information, correctly identified the issue category, and did not give misleading or wrong policy information.

| Score Range | Description |
|---|---|
| **18–20** | All information provided was verifiably correct. Policy details, pricing, and timelines stated accurately. No corrections needed. |
| **14–17** | Minor imprecision in one statement (e.g., slightly wrong timeframe) but core information correct. Customer was not materially misled. |
| **10–13** | One clearly incorrect statement made. Customer may have acted on wrong information. Partial correction was made later in call. |
| **5–9** | Significant wrong information delivered without correction. Customer was materially misled on policy, pricing, or timelines. |
| **0–4** | Multiple incorrect statements. Customer was actively misled. Constitutes a compliance risk. |

**Automatic deductions:**
- −10: Injected wrong information (e.g., stating 90-day refund policy when policy is 30 days)
- −5: Wrong information flagged in failure indicators without correction
- −4: Agent loop detected (indicates agent lost track of context)

---

## Dimension 2: Empathy (0–20)

**Definition:** The agent acknowledged the customer's emotional state, responded with appropriate tone, and avoided inappropriate positivity during distress.

| Score Range | Description |
|---|---|
| **18–20** | Agent recognized and explicitly acknowledged customer frustration or distress. Tone was warm and human throughout. Resolution pace matched emotional urgency. |
| **14–17** | Agent was professional and courteous. Acknowledged the issue impact. One minor tone mismatch (e.g., slightly too formal when customer was upset). |
| **10–13** | Agent was neutral but not empathetic. Did not acknowledge emotional state. Customer left feeling unheard, though technically served. |
| **5–9** | Agent tone diverged from customer's emotional state. Used overly positive language during distress ("That's wonderful!"). Customer may have felt dismissed. |
| **0–4** | Significant sentiment mismatch. Agent was upbeat or dismissive during customer distress. Call abandoned or customer expressed anger at agent's response. |

**Automatic deductions:**
- −8: Sentiment mismatch failure mode flagged
- −6: Call abandoned (customer disengaged without resolution)
- Scaled by agent_performance score (−4 to +4 range)

---

## Dimension 3: Efficiency (0–20)

**Definition:** The call reached a clear outcome without unnecessary delays, excessive agent holds, or circular dialogue.

| Score Range | Description |
|---|---|
| **18–20** | Issue identified quickly. Resolution steps were direct and appropriate. Call duration was at or below category average. No unnecessary holds. |
| **14–17** | Slightly longer than average but all time was productive. One brief hold or clarification loop. Customer was kept informed of delays. |
| **10–13** | Noticeable inefficiency. Extended hold times, repeated questions already answered, or unclear reasoning communicated to customer. |
| **5–9** | Significant delays. Customer had to repeat information multiple times. Multiple unnecessary holds. Agent appeared confused about how to proceed. |
| **0–4** | Call was dramatically longer than category norm (>2σ). Excessive latency messages ("still processing..."). Customer expressed frustration at wait times. |

**Automatic deductions:**
- −8: Call duration exceeds category mean + 2σ
- −6: Excessive latency failure mode injected
- +2: Resolved call with duration below mean − 0.5σ (efficiency bonus)

---

## Dimension 4: Resolution (0–20)

**Definition:** The customer's stated issue was addressed, and the call concluded with a clear, confirmed outcome.

| Score Range | Description |
|---|---|
| **18–20** | Issue fully resolved within the call. Customer confirmed resolution. Appropriate follow-up steps communicated (e.g., "refund within 3–5 days"). |
| **14–17** | Issue mostly resolved. Minor follow-up required. Customer understood next steps. Escalation (if any) was appropriate and smooth. |
| **10–13** | Partial resolution. Issue addressed but not confirmed. Customer uncertain about outcome. Or: escalation triggered but poorly executed. |
| **5–9** | Issue unresolved at call end. No clear next steps communicated. Customer left with incomplete information or incorrect expectations. |
| **0–4** | Call abandoned without any resolution attempt, or escalation was inappropriate (customer had high confidence/sentiment, shouldn't have been escalated). |

**Computation:** `resolution_confidence × 20`, then:
- −5: Incomplete resolution flag (resolved call with low confidence)
- −4: Wrong escalation flag (escalated call with high confidence)

---

## Dimension 5: Compliance (0–20)

**Definition:** The agent followed all applicable policies, escalation protocols, data handling rules, and did not make unauthorized commitments.

| Score Range | Description |
|---|---|
| **18–20** | Full policy compliance. All escalations followed proper protocol. No unauthorized offers or commitments made. Customer identity verified appropriately. |
| **14–17** | One minor procedural gap (e.g., slightly early in verification flow). No policy violations. All commitments within agent authority. |
| **10–13** | One compliance concern noted (e.g., vague about data retention, skipped identity verification step). No material violation. |
| **5–9** | Clear policy misstatement (wrong refund window, wrong feature availability). Or improper escalation (escalated without following warm-transfer protocol). |
| **0–4** | Agent made unauthorized commitments, provided incorrect policy information as fact, or bypassed mandatory verification steps. |

**Automatic deductions:**
- −8: Wrong information failure mode (incorrect policy stated)
- −4: Wrong escalation mode (improper escalation protocol)
- −3: Agent loop failure (failure to follow proper resolution protocol)

---

## Composite Scoring Guide

| Total Score | Grade | Action |
|---|---|---|
| **90–100** | Excellent | No action required. Flag as positive training example. |
| **80–89** | Good | Minor coaching note if recurring pattern in a single dimension. |
| **70–79** | Acceptable | Monitor for trends. One-on-one feedback if score persists below 75. |
| **60–69** | Needs Improvement | QA analyst review within 5 business days. Root cause identified. |
| **50–59** | Poor | Immediate QA review. Customer follow-up may be required. |
| **< 50** | Critical | Escalate to product team. Customer proactive outreach. Model flag. |

---

## How to Use This Rubric (Human Reviewers)

1. **Load the call** in the review interface with the full transcript visible
2. **Score each dimension independently** — do not let the overall outcome bias sub-scores
3. **Use the automatic scoring as a baseline** — adjust ±3 points based on transcript nuance
4. **Document specific utterances** that drove score adjustments in the notes field
5. **Mark the call as a training candidate** if the score diverges from the automated score by >10 points (indicates a model calibration gap)
6. **Flag for proactive outreach** if total score < 50 and the customer expressed distress or was given wrong information

---

## Calibration Notes

- Re-calibrate this rubric against human reviewer consensus every quarter
- Empathy scores tend to be the most subjective — use the specific deduction rules as anchors
- Compliance scoring should be reviewed by a legal/policy stakeholder before each rubric version release
- The rubric is intentionally conservative on accuracy: a single wrong policy statement caps accuracy at ≤13, because customer-facing errors have asymmetric impact
