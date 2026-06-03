# Growth Brief: AI Agent Activation & Funnel Optimization
**AI Product Analyst Portfolio — Synthetic Case Study**
*Prepared: Q1 2024 | Data: 5,000 synthetic users | Period: Jan–Mar 2024*

---

## Executive Summary

User activation is the primary growth constraint for this AI agent product. Of every 100 users who sign up, fewer than **40 complete their first agent run** — the event that most strongly predicts long-term retention and revenue. Two onboarding steps account for the majority of this loss, and the drop-off is disproportionately concentrated in the "casual user" segment (40% of signups) where a targeted intervention can recoup the most volume.

**Three actions are recommended:**
1. Streamline onboarding Step 3 (A/B test ready to ship)
2. Launch a Day-3 activation nudge email for stalled casual users
3. Build a referral programme anchored to the power-user cohort

Conservatively, these interventions could lift overall activation by **8–12 percentage points** and Day-30 retention by **4–6 percentage points** within one quarter.

---

## 1. Funnel Analysis

### 1.1 Overall Funnel Drop-off

| Step | Users | Cumulative % | Step Drop |
|------|------:|:------------:|:---------:|
| Signed Up | ~5,000 | 100% | — |
| Onboarding Step 1 | ~4,000 | ~80% | −20% |
| Onboarding Step 2 | ~2,900 | ~58% | −22% |
| Onboarding Step 3 | ~2,100 | ~42% | −16% |
| First Agent Run | ~1,900 | ~38% | −4% |
| Second Agent Run | ~1,500 | ~30% | −8% |
| Retained Day 7 | ~1,100 | ~22% | −8% |
| Retained Day 30 | ~600 | ~12% | −10% |

*Note: Values are approximate; run `analysis.ipynb` for exact figures from your generated dataset.*

**Key observations:**
- The **largest single drop** occurs at Onboarding Step 2 → Step 3 (−22 pp). This is the point where users must configure agent parameters — the highest-friction task in the flow.
- Users who complete `first_agent_run` convert to Day-7 retention at ~60%, confirming activation as the leading indicator of retention.
- Only **12% of all signups reach Day-30 retention** — a critical gap given acquisition cost.

### 1.2 Where Is the Biggest Opportunity?

The funnel narrows most aggressively in the **onboarding → activation** phase (Steps 1–5). The drop from 100% to 38% activation represents the largest addressable loss. Post-activation retention is comparatively healthy: once users run their first agent, ~60% are still active at Day 7.

**Implication:** Investments in top-of-funnel (more signups) will have diminishing returns until the activation bottleneck is resolved.

---

## 2. Cohort Analysis: Three High-Drop-off Segments

### Cohort 1: Casual Users (40% of signups — highest priority)

| Metric | Value |
|--------|------:|
| Onboarding completion | ~40% |
| Activation rate | ~50% |
| Day-7 retention | ~35% |
| Day-30 retention | ~15% |

Casual users enter with moderate intent but are deterred by configuration complexity in Step 3. They represent the **highest-volume improvement opportunity** — even a 10 pp lift in their activation rate would add ~200 activated users per 5,000 signups.

**Stall point:** Onboarding Step 3 (agent configuration). Most drop here within the first session.

**Root cause hypothesis:** The agent configuration UI requires domain knowledge (API keys, use-case selection, prompt templates) that casual users do not have at sign-up time.

### Cohort 2: Churned Users (30% of signups — acquisition quality issue)

| Metric | Value |
|--------|------:|
| Onboarding Step 1 completion | ~50% |
| Activation rate | ~10% |
| Day-7 retention | ~5% |
| Day-30 retention | ~2% |

Half of churned users never complete even Step 1 — suggesting the issue begins before the product is experienced. This is an **acquisition quality problem**, not a product problem. These users likely arrive with misaligned expectations.

**Stall point:** Between sign-up and Onboarding Step 1.

**Root cause hypothesis:** Paid social traffic (overrepresented in this cohort) drives low-intent users who are attracted by ad creative but not by the product's actual value proposition.

**Recommendation:** Audit paid social creatives to align messaging with product reality. Consider adding a qualification step (use-case question) at sign-up to segment intent.

### Cohort 3: Casual Users by Channel — Paid Social Subset

Channel-level analysis reveals that **paid social casual users** have the worst retention quality index (Day-30/Day-7 ratio ≈ 0.35 vs. 0.55 for referral). This sub-segment accounts for a disproportionate share of mid-funnel drop-off and is the highest-cost cohort to acquire.

**Recommendation:** Shift paid budget toward referral amplification and organic SEO, where retention quality is measurably higher.

---

## 3. A/B Test Proposal

### Test Name: Streamlined Onboarding (Skip Step 3)

**Problem:** Onboarding Step 3 (agent configuration) causes the second-largest funnel drop. Users are asked to configure advanced settings before they understand the product's value.

**Hypothesis:** If we replace the mandatory Step 3 configuration screen with an intelligent defaults flow (pre-populated configuration based on use-case selected at sign-up), activation rate will increase by ≥5 percentage points without degrading Day-7 retention.

### Test Design

| Parameter | Value |
|-----------|-------|
| **Type** | Two-arm randomised controlled trial (50/50 split) |
| **Unit of randomisation** | User (randomised at sign-up) |
| **Control** | Existing 3-step onboarding with manual Step 3 configuration |
| **Treatment** | 2-step onboarding with intelligent defaults (Step 3 bypassed) |
| **Primary metric** | Activation rate = `first_agent_run` / `signed_up` |
| **Guardrail metric** | Day-7 retention rate ≥ baseline (non-inferiority) |
| **Secondary metrics** | Second agent run rate, Day-30 retention, time-to-activation |

### Statistical Parameters

| Parameter | Value |
|-----------|-------|
| Significance level α | 0.05 (two-sided) |
| Power | 80% |
| Baseline activation rate | ~38% |
| Minimum detectable effect (MDE) | +5 pp absolute (+13% relative) |
| **Required sample per arm** | ~2,000 users |
| **Required total sample** | ~4,000 users |
| **Estimated duration** | 14–21 days at current traffic |

### Decision Rules

- **Ship** if: activation rate significantly increases (p < 0.05) AND Day-7 retention is non-inferior (≥ baseline − 2 pp)
- **Iterate** if: activation increases but Day-7 retention degrades (investigate whether defaults reduce agent quality)
- **Kill** if: no significant activation lift after full sample collected

### Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Intelligent defaults produce low-quality agent runs, degrading retention | Monitor secondary metric (second agent run rate) as early signal |
| Novelty effect inflates early results | Enforce minimum 14-day runtime; analyse by cohort signup day |
| Sample ratio mismatch | Monitor daily split ratios; alert if deviation > 1% |

---

## 4. Intervention Roadmap

### Intervention 1: Streamlined Onboarding (A/B Test — 2–3 weeks)
- **Owner:** Product + Engineering
- **Effort:** Medium (2-week sprint)
- **Estimated activation lift:** +5–8 pp
- **Estimated Day-7 retention impact:** Neutral to +2 pp
- **Rationale:** Highest-volume impact; directly addresses the second-largest funnel drop

### Intervention 2: Day-3 Activation Nudge Email (Quick Win — 1 week)
- **Target segment:** Users who completed Step 1 but have not run `first_agent_run` within 72 hours
- **Message:** Personalised email with a pre-configured agent template matching their stated use case
- **Owner:** Growth + CRM
- **Effort:** Low (email template + trigger logic)
- **Estimated activation lift for targeted segment:** +3–5 pp
- **Rationale:** Catches casual users in the consideration window before they churn; low engineering cost

### Intervention 3: Power-User Referral Programme (Strategic — 4–6 weeks)
- **Target segment:** Power users who have reached Day-30 retention
- **Mechanic:** In-product referral prompt with incentive (extended features or usage credits)
- **Owner:** Product + Marketing
- **Effort:** Medium-high (referral tracking, incentive logic)
- **Estimated impact:** Shift acquisition mix toward higher-intent users; improve Day-30 retention of new cohorts by 3–5 pp over 2 quarters
- **Rationale:** Referral traffic has the highest retention quality index in current data; organic referral loops reduce paid social dependency

---

## 5. Summary Dashboard (Key Metrics to Track)

| Metric | Current | 90-Day Target | Intervention |
|--------|:-------:|:-------------:|:-------------|
| Overall activation rate | ~38% | 46% | Streamlined onboarding + nudge email |
| Casual user activation rate | ~50% | 60% | Streamlined onboarding |
| Day-7 retention | ~22% | 28% | Activation improvements (activated users retain better) |
| Day-30 retention | ~12% | 16% | Retention-quality acquisition shift |
| Time-to-first-agent-run (median) | ~1.5 h | < 45 min | Streamlined onboarding |

---

*This brief is based on synthetic data generated for portfolio demonstration purposes. All figures are illustrative of realistic product analytics patterns.*
