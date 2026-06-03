# Frontier vs. Local LLM Decision Framework for AI Product Teams

**Version 1.0** | Enterprise GenAI Strategy | AI Product Management

---

## Purpose

This framework helps AI product teams make defensible, data-driven decisions about whether to use frontier model APIs (GPT-4o, Claude, Gemini) or deploy open-source models on local/private infrastructure. The decision has significant implications for cost, latency, data governance, and engineering complexity.

There is no universal right answer. The framework provides a repeatable process to evaluate the tradeoff for a specific use case at a specific scale.

---

## Part 1: When to Use Frontier APIs

### Ideal Conditions

**Use frontier APIs when one or more of the following apply:**

1. **Volume is low or unpredictable.** Below ~1,000–2,500 calls/day (depending on token density), the fixed cost of local GPU infrastructure exceeds variable API costs. Frontier APIs have zero CapEx and scale to zero automatically.

2. **Task requires peak capability.** Complex reasoning, multi-step agentic workflows, nuanced creative writing, or tasks where quality differences between a 7B and a 70B+ model meaningfully impact user outcomes. Legal drafting, financial analysis, and novel code generation often fall here.

3. **Time-to-market is the primary constraint.** A frontier API call requires zero MLOps infrastructure. For prototypes, MVPs, and pilot programs, the 2–6 weeks saved by avoiding local deployment has real business value.

4. **Workload is bursty or seasonal.** A customer support spike during the holiday season or a legal review surge during M&A activity is expensive to over-provision for locally. APIs absorb spikes at the same per-token rate.

5. **No sensitive data is involved.** If the data processed is not regulated (no PII, no trade secrets, no attorney-client privilege), the privacy objection to frontier APIs disappears.

### Risk Factors for Frontier APIs

- **Vendor lock-in**: API contracts, model versioning changes, deprecations
- **Cost at scale**: Variable costs grow linearly with volume; no economies of scale
- **Latency ceiling**: Round-trip network latency adds 150–400ms unavoidably
- **Rate limits**: Tier-based throttling can block high-throughput production workloads

---

## Part 2: When to Go Local

### Ideal Conditions

**Deploy local/private models when three or more of the following apply:**

1. **Volume exceeds breakeven.** Once monthly API costs would exceed the monthly amortized cost of GPU infrastructure (typically $2,000–$4,500/month for a single server), local deployment is economically superior. For token-heavy use cases like document summarization, this breakeven can occur at under 1,000 calls/day.

2. **Data is regulated or sensitive.** Healthcare (HIPAA), finance (SOX, GLBA), legal (attorney-client privilege), and HR (employment law) use cases often cannot send data to third-party APIs under existing compliance frameworks. Local deployment is the only viable path.

3. **Latency requirements are strict.** Applications requiring sub-100ms response times (real-time coding autocomplete, live customer chat with SLA commitments) can achieve this locally but not over a frontier API network round-trip.

4. **The task is narrow and well-defined.** Resume screening, invoice parsing, sentiment classification, and similar structured tasks do not require GPT-4-level intelligence. A fine-tuned 7B or 13B model achieves equivalent or better accuracy at 1/20th the cost.

5. **You have or can hire MLOps capacity.** Local deployment requires model serving infrastructure (vLLM, TGI, Ollama), monitoring, version management, and periodic retraining. Without a team capable of owning this, the operational overhead erodes the cost savings.

### Risk Factors for Local Deployment

- **Upfront CapEx**: $10,000–$50,000+ for GPU hardware if purchasing; months of procurement lead time
- **Maintenance burden**: Model updates, infrastructure patching, serving optimization
- **Quality gap on complex tasks**: Smaller models underperform on nuanced reasoning; requires validation
- **Scaling complexity**: Horizontal scaling requires orchestration (Kubernetes, Ray Serve)

---

## Part 3: Key Questions to Ask Before Deciding

Work through these questions with your team before committing to either path:

### Volume & Economics
- What is our current call volume, and what is our 12-month forecast?
- What is the average token count per call (input + output)?
- At current prices, what would our monthly frontier API bill be?
- What would a single GPU server cost us per month (CapEx amortized over 3 years + power + ops)?
- At what call volume does local become cheaper? (Calculate the breakeven.)

### Data & Compliance
- Does this use case process PII, PHI, legally privileged, or trade-secret data?
- Do our enterprise contracts or customer DPAs prohibit sending this data to third-party APIs?
- Has legal reviewed the data handling implications?

### Quality Requirements
- What is the minimum acceptable output quality for this use case?
- Have we benchmarked a 7B/13B open-source model against our actual task?
- Is the quality gap between local and frontier models meaningful in production, or theoretical?

### Operational Readiness
- Do we have MLOps engineers who can own model serving infrastructure?
- What is our acceptable deployment timeline — days, weeks, or months?
- Do we have GPU hardware available, or would this require procurement?

### Strategic Factors
- Is this a core competency we want to build internally, or a commodity capability to outsource?
- How important is model customization (fine-tuning) to our roadmap?
- What is the cost of getting this wrong (downtime, quality failures, compliance breach)?

---

## Part 4: The Decision Matrix Explained

The cost model notebook includes a weighted scoring matrix across five dimensions. Here is how to interpret and adapt it:

| Dimension | Weight | Description |
|---|---|---|
| Cost Efficiency | 30% | Unit economics at current and projected volume |
| Latency | 20% | p95 response time vs. application requirement |
| Output Quality | 20% | Task-specific accuracy, evaluated on real data |
| Data Privacy | 15% | Regulatory and contractual data handling constraints |
| Maintenance Overhead | 15% | MLOps complexity relative to team capacity |

**Scoring scale: 1 (poor) to 5 (excellent)** for each dimension, for each model option.

**How to adapt the weights:** If your use case involves regulated data, raise the Privacy weight to 25–30% and reduce Cost or Latency. If you are building a real-time user-facing product, raise Latency to 30% and reduce Maintenance.

**Interpretation guidance:**
- If frontier scores 3.5+ on the weighted matrix: start with the API, revisit at 6-month scale review
- If local scores higher but within 0.5 points: the margin may not justify migration cost; use API
- If local scores 1.0+ higher: build the business case for infrastructure investment
- If Privacy scores 1 for frontier (regulated data): local is required regardless of other scores

---

## Part 5: Risk Factors Summary Table

| Risk | Frontier API | Local Deployment |
|---|---|---|
| Cost overrun at scale | High | Low |
| Data privacy breach | Medium–High | Low |
| Vendor dependency | High | Low |
| Quality on complex tasks | Low | Medium |
| Operational complexity | Low | High |
| Time to production | Low | Medium–High |
| Latency at p99 | Medium | Low |
| Scaling flexibility | Low (rate limits) | Medium (hardware bound) |

---

## Quick Reference: Decision Summary

```
Is data regulated or sensitive?
  YES → Local deployment required. Evaluate cost/quality separately.
  NO  → Continue...

Is monthly API cost > $3,000 at current or 6-month projected volume?
  YES → Build breakeven model. Local likely justified.
  NO  → Continue...

Is p95 latency requirement < 150ms?
  YES → Local deployment likely required.
  NO  → Continue...

Does the task require frontier-level reasoning (complex, multi-step, creative)?
  YES → Use frontier API. Revisit at scale.
  NO  → Benchmark a local 7B–13B model. If quality passes, go local.

Do you have MLOps capacity to own local infrastructure?
  NO  → Use frontier API until capacity exists or hire first.
  YES → Proceed with local deployment plan.
```

---

*This framework is a starting point, not a formula. Use it to structure the conversation with your team, surface the right questions, and document your decision rationale. Revisit the decision every 6 months as volumes change and model quality improves.*
