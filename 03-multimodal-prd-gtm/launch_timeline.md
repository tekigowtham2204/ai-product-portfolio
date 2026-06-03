# Launch Timeline
## HireIQ Vision — 16-Week Phased Launch Plan

---

| Field | Value |
|---|---|
| **Document Version** | 1.1 |
| **Author** | Gowtham Teki, Senior Product Manager |
| **Created** | 2026-02-15 |
| **Last Updated** | 2026-06-03 |
| **Program Start (Week 1)** | 2026-06-09 |
| **Target GA Date (Week 11)** | 2026-08-17 |
| **Status** | Approved — In Execution |

---

## Phase Overview

| Phase | Weeks | Dates | Audience | Exit Gate |
|---|---|---|---|---|
| Internal Alpha | 1–4 | Jun 9 – Jul 4 | ~15 internal users | PM + Eng + Legal sign-off |
| Closed Beta | 5–10 | Jul 7 – Aug 15 | 15 enterprise design partners (~45 users) | PM + VP Product + VP Sales sign-off |
| General Availability | 11–16 | Aug 17 – Sep 26 | All Enterprise + Growth tier customers | VP Product sign-off |

---

## Phase 1: Internal Alpha — Weeks 1–4

### Objectives

1. Validate end-to-end functionality of image ingestion, multimodal query, and resume intelligence modules (FR-001 through FR-016)
2. Establish performance baselines: upload success rate, time to first token, error rate
3. Surface and resolve critical bugs before external exposure
4. Validate image pipeline security with internal security review

### Week-by-Week Tasks

#### Week 1 (Jun 9–13) — Infrastructure & Staging

| Task | Owner | Status |
|---|---|---|
| Multimodal LLM API vendor: finalize selection (GPT-4o vs. Claude 3.5 Sonnet) | ML Lead (Raj Iyer) | In progress |
| Image ingestion pipeline deployed to staging environment | Backend (Daniel Osei) | In progress |
| S3-compatible object storage provisioned with encryption at rest | Infra (Alex Park) | Not started |
| Image upload UI (FR-001, FR-002, FR-003) deployed to internal staging | Frontend (Carmen Liu) | In progress |
| Audit log schema extension (image hash, dimensions, user ID) | Data (Yemi Adewale) | Not started |
| LLM vendor DPA: procurement review initiated | Legal (Leah Torres) | In progress |

#### Week 2 (Jun 16–20) — Core Feature Integration

| Task | Owner | Status |
|---|---|---|
| Multimodal query endpoint integrated with LLM API (FR-008, FR-010) | Backend | Not started |
| Image validation and compression pipeline (FR-004, FR-006) | Backend | Not started |
| Session context store implemented (FR-022) | Backend | Not started |
| Resume structured extraction (FR-013) — initial version | ML (Priyanka Shah) | Not started |
| Internal security review of image upload endpoints | Security (Jordan Tran) | Not started |
| EEO system prompt review: no protected characteristic inference | Legal + ML | Not started |

#### Week 3 (Jun 23–27) — Internal Dogfood Launch

| Task | Owner | Status |
|---|---|---|
| Internal alpha deployed to production (behind feature flag) | Eng | Not started |
| Internal testers onboarded (HireIQ recruiting team + PM/Eng dogfood) | PM | Not started |
| In-product feedback mechanism (thumbs-up/down) live | Frontend | Not started |
| Daily bug triage process established | Eng Lead | Not started |
| Image compression benchmark testing (20 diverse resume images) | ML | Not started |
| PDF extraction (FR-007) implemented and tested | Backend | Not started |

#### Week 4 (Jun 30 – Jul 4) — Alpha Hardening & Gate Review

| Task | Owner | Status |
|---|---|---|
| All alpha bugs triaged; P0 count reviewed | Eng Lead | Not started |
| Performance baseline report: upload success rate, TTFToken p50/p95 | Data | Not started |
| Security review sign-off from Jordan Tran | Security | Not started |
| Internal user feedback synthesized by PM | PM | Not started |
| Alpha exit gate meeting: PM + Eng Lead + Legal | PM | Not started |
| Beta partner selection finalized (15 accounts confirmed) | PM + Account Mgmt | Not started |

### Phase 1 Exit Criteria

All of the following must be true before advancing to Phase 2:

- [ ] Zero open P0 bugs
- [ ] Image upload success rate ≥97% in internal testing (min. 200 test uploads)
- [ ] Time to first token p95 ≤4.0 seconds
- [ ] Internal security review completed and sign-off received
- [ ] At least 50 multimodal queries submitted internally with results reviewed by PM and ML
- [ ] DPA procurement review with LLM vendor at advanced stage (contract not required for alpha entry but required for beta)
- [ ] Beta partner list confirmed (15 accounts)

---

## Phase 2: Closed Beta — Weeks 5–10

### Objectives

1. Validate product-market fit with representative enterprise customers
2. Collect quantitative adoption and quality metrics (thumbs-up rate, time-on-task, adoption curves)
3. Surface usability issues through real-world usage patterns not captured in internal testing
4. Complete all compliance documentation required for GA
5. Generate case study material and testimonials for GA launch

### Week-by-Week Tasks

#### Week 5 (Jul 7–11) — Beta Launch

| Task | Owner | Status |
|---|---|---|
| Beta accounts feature-enabled via RBAC (admin configuration) | Eng + AM | Not started |
| Kickoff calls completed with all 15 beta accounts (45 min each) | PM + CSM | Not started |
| Beta onboarding guide delivered (PDF + in-app walkthrough) | PM + Design | Not started |
| Dedicated Slack channel created per beta account | CSM (Grace Obi) | Not started |
| Beta metrics dashboard live (Amplitude): adoption, error rate, thumbs-up | Data | Not started |
| All remaining functional requirements (FR-017 through FR-025) deployed to beta | Eng | Not started |

#### Week 6 (Jul 14–18) — Early Signal Review

| Task | Owner | Status |
|---|---|---|
| Week 1 check-in calls with all beta accounts (30 min each) | PM + CSM | Not started |
| First beta metrics review: adoption, error types, top queries | PM | Not started |
| Critical bugs from beta week 1 triaged and resolved | Eng | Not started |
| Whiteboard analysis (FR-019) accuracy reviewed against beta submissions | ML | Not started |
| EU data residency routing tested with EU beta partners | Infra | Not started |

#### Week 7–8 (Jul 21 – Aug 1) — Beta Iteration

| Task | Owner | Status |
|---|---|---|
| P0/P1 bugs resolved on 48-hour SLA | Eng | Ongoing |
| LLM vendor DPA finalized and signed | Legal | Not started |
| Customer-facing DPA addendum finalized and available | Legal | Not started |
| Help center documentation drafted (beta review by CSM) | CS + PM | Not started |
| Sales enablement materials: demo script, competitive battlecard | Marketing (Elena V) | Not started |
| Resume extraction accuracy benchmark: 100-image test set evaluation | ML | Not started |

#### Week 9 (Aug 4–8) — Mid-Beta Assessment

| Task | Owner | Status |
|---|---|---|
| Mid-beta structured survey deployed to all beta users (Typeform, 10 questions) | PM | Not started |
| Survey results synthesized and reviewed with VP Product | PM | Not started |
| Feature NPS calculated from beta cohort | PM | Not started |
| Adjustments to system prompt or UX based on mid-beta feedback | PM + ML + Design | Not started |
| Pricing model review with Finance: confirm tier inclusion strategy | PM + Finance | Not started |
| Sales team training session: demo + competitive positioning | Marketing + Sales | Not started |

#### Week 10 (Aug 11–15) — Beta Exit & GA Preparation

| Task | Owner | Status |
|---|---|---|
| Exit interviews with all 15 beta accounts (60 min each) | PM + CSM | Not started |
| Beta metrics final report: adoption, thumbs-up rate, NPS, error rate | PM + Data | Not started |
| Beta exit gate meeting: PM + VP Product + VP Sales + Legal | PM | Not started |
| Case study interviews completed (target: 5 beta accounts) | Marketing | Not started |
| Help center documentation finalized and published to staging | CS | Not started |
| Support team training completed (Tier 1 + Tier 2) | CS Lead | Not started |
| GA monitoring dashboards and alerting configured | Infra + Data | Not started |
| Rollback plan documented and rehearsed | Eng | Not started |

### Phase 2 Exit Criteria

All of the following must be true before advancing to Phase 3:

- [ ] Image query success rate (thumbs-up %) ≥75% (measured on minimum 200 rated queries)
- [ ] Zero open P0 bugs; zero open P1 bugs
- [ ] Time to first token p95 ≤3.0 seconds
- [ ] Feature NPS from beta cohort ≥35
- [ ] LLM vendor DPA signed
- [ ] Customer DPA addendum finalized and reviewed by Legal
- [ ] Legal sign-off on EEO system prompt guardrails
- [ ] At least 3 written testimonials/case study approvals from beta accounts
- [ ] Sales enablement materials complete and reviewed by VP Sales
- [ ] Support team trained; Tier 1 support documentation live
- [ ] Help center documentation reviewed, published, and indexed
- [ ] GA monitoring infrastructure live with alerting tested

---

## Phase 3: General Availability — Weeks 11–16

### Objectives

1. Execute controlled rollout to all eligible customers with zero P0 incidents
2. Achieve ≥35% feature adoption among eligible users within 30 days
3. Validate all primary KPIs trending toward 6-month targets
4. Establish steady-state monitoring and support processes
5. Collect early GA feedback to inform v1.1 roadmap prioritization

### Week-by-Week Tasks

#### Week 11 (Aug 17–22) — Canary Release (10%)

| Task | Owner | Status |
|---|---|---|
| Feature flag enabled for 10% of eligible Enterprise + Growth accounts (randomized) | Eng | Not started |
| In-product onboarding tour live for new users | Design + Frontend | Not started |
| GA announcement email sent to all eligible customers | Marketing | Not started |
| Press release + blog post published | Marketing | Not started |
| Daily canary metrics review: error rate, adoption, latency | PM + Eng | Not started |
| On-call engineering rotation active (24/7 coverage during ramp) | Eng | Not started |

#### Week 12 (Aug 24–29) — 25% Rollout (Conditional)

| Task | Owner | Status |
|---|---|---|
| Canary review gate: error rate <0.5%, thumbs-up ≥75% | PM + Eng | Not started |
| If gate passed: expand to 25% | Eng | Not started |
| Customer success activation outreach: proactive outreach to newly-enabled accounts | CSM | Not started |
| Top canary issues triaged and resolved | Eng | Not started |
| Sales team: GA announcement to pipeline, launch deck updated | Sales | Not started |

#### Week 13 (Aug 31 – Sep 5) — 50% Rollout

| Task | Owner | Status |
|---|---|---|
| 25% review gate: error rate <0.5%, no new P1 issues | PM + Eng | Not started |
| If gate passed: expand to 50% | Eng | Not started |
| First GA weekly metrics report distributed | PM | Not started |
| In-product tooltip campaign: feature discovery for low-engagement users | Marketing + PM | Not started |

#### Week 14 (Sep 7–12) — 100% Rollout

| Task | Owner | Status |
|---|---|---|
| 50% review gate assessment | PM + Eng | Not started |
| If gate passed: enable for 100% of eligible accounts | Eng | Not started |
| GA completion announcement to internal stakeholders | PM | Not started |
| On-call coverage reduced to business hours + PagerDuty | Eng | Not started |

#### Weeks 15–16 (Sep 14–26) — Steady State & Iteration

| Task | Owner | Status |
|---|---|---|
| 30-day post-GA metrics review (vs. targets) | PM + Data | Not started |
| v1.1 roadmap kickoff: incorporate GA feedback and beta learnings | PM | Not started |
| First customer QBRs with Vision usage data included | CSM | Not started |
| Standard tier upgrade campaign: Vision as upsell trigger | Marketing + Sales | Not started |
| Retrospective: 16-week program retrospective with full team | PM | Not started |

### Phase 3 Exit Criteria (Full GA Health Check at Week 16)

- [ ] Feature enabled for 100% of eligible customers
- [ ] No open P0 incidents in past 2 weeks
- [ ] 30-day adoption: ≥35% of eligible users have submitted ≥1 image query
- [ ] Image query success rate (thumbs-up) ≥75% — GA cohort
- [ ] Platform-level NPS: no decline greater than 5 points vs. pre-launch baseline
- [ ] Time to first token p95 ≤3.0 seconds — sustained under full load
- [ ] v1.1 roadmap draft approved by VP Product

---

## Cross-Functional RACI Matrix

**R** = Responsible (does the work)  
**A** = Accountable (final decision authority)  
**C** = Consulted (provides input)  
**I** = Informed (kept up to date)

| Activity | PM | ML Eng | Backend Eng | Frontend Eng | Data Eng | Design | GTM/Mktg | Legal | CS/Support | Exec |
|---|---|---|---|---|---|---|---|---|---|---|
| LLM vendor selection | C | R | C | — | — | — | — | C | — | A |
| Image ingestion pipeline | C | C | R | — | — | — | — | — | — | — |
| Multimodal UI (upload, preview) | A | — | C | R | — | R | — | — | — | — |
| Session context store | C | — | R | — | — | — | — | — | — | — |
| Resume extraction accuracy | A | R | — | — | — | — | — | — | — | — |
| Audit log schema | A | — | C | — | R | — | — | I | — | — |
| System prompt (EEO guardrails) | A | R | — | — | — | — | — | C | — | — |
| DPA with LLM vendor | C | I | — | — | — | — | — | R | — | A |
| Customer DPA addendum | C | — | — | — | — | — | — | R | C | A |
| Beta partner selection | R | — | — | — | — | — | C | — | C | A |
| Beta onboarding | R | — | — | — | — | — | — | — | R | — |
| Help center documentation | A | — | — | — | — | — | C | — | R | — |
| Sales enablement materials | C | — | — | — | — | — | R | — | — | A |
| Support team training | A | — | — | — | — | — | — | — | R | — |
| GA monitoring dashboards | C | — | C | — | R | — | — | — | — | — |
| Rollout feature flag management | A | — | R | — | — | — | — | — | — | — |
| GA announcement / PR | C | — | — | — | — | — | R | C | — | A |
| Post-launch metrics reporting | R | — | — | — | C | — | C | — | — | A |
| v1.1 roadmap | R | C | C | C | C | C | C | — | C | A |

---

## Key Milestones Table

| Milestone | Target Date | Owner | Dependencies |
|---|---|---|---|
| LLM vendor selected | Jun 13 (Week 1) | ML Lead | Benchmark evaluation complete |
| Image ingestion pipeline on staging | Jun 13 (Week 1) | Backend | S3 storage provisioned |
| Internal alpha launched | Jun 23 (Week 3) | PM + Eng | Weeks 1–2 tasks complete |
| Security review sign-off | Jul 4 (Week 4) | Security | Internal alpha live |
| Alpha exit gate passed | Jul 4 (Week 4) | PM | All alpha exit criteria met |
| Beta partners confirmed (15 accounts) | Jul 4 (Week 4) | PM + AM | Partner scoring complete |
| Closed beta launched | Jul 7 (Week 5) | PM + Eng | Alpha gate passed |
| LLM vendor DPA signed | Aug 1 (Week 8) | Legal | Procurement review complete |
| Mid-beta survey results reviewed | Aug 8 (Week 9) | PM | Survey distributed week 9 |
| Sales team trained | Aug 8 (Week 9) | Marketing | Enablement materials complete |
| Support team trained | Aug 15 (Week 10) | CS Lead | Help center docs complete |
| Beta exit gate passed | Aug 15 (Week 10) | PM | All beta exit criteria met |
| GA canary launch (10%) | Aug 17 (Week 11) | PM + Eng | Beta gate passed |
| Full GA rollout (100%) | Sep 12 (Week 14) | PM + Eng | Canary/ramp gates passed |
| 30-day post-GA metrics review | Sep 17 (Week 15) | PM | 30 days from GA start |
| v1.1 roadmap draft approved | Sep 26 (Week 16) | PM | GA learnings synthesized |

---

## Escalation Protocol

**If a phase gate is not met:**

1. PM documents the specific criteria that are not met and the estimated time to resolution
2. PM schedules an emergency gate review with VP Product within 48 hours
3. Options considered: (a) slip the phase start date, (b) launch with reduced scope, (c) escalate to exec if timeline impact affects customer commitments
4. All gate delays are documented in the launch log with root cause

**If a P0 incident occurs during GA rollout:**

1. On-call engineer pages PM and Eng Lead immediately
2. Feature flag to disable image processing is available and can be toggled within 15 minutes
3. Text-only functionality continues during image processing disable
4. Customer communication template pre-drafted and ready to send within 2 hours of incident confirmation
5. Post-mortem required within 5 business days of resolution
