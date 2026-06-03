# Enterprise GenAI Unit Economics & Model Cost Audit

**AI Product Analyst Portfolio Project** | Cost Modeling | Build vs. Buy Analysis | LLM Infrastructure

---

## Overview

This project delivers a rigorous unit economics framework for enterprise GenAI deployments. It answers the most common question AI product teams face: **when does it make financial sense to run local/open-source models versus paying for frontier API access?**

The analysis covers five high-volume enterprise use cases, compares four model tiers, and produces a repeatable decision framework for product teams to adapt to their own workloads.

---

## Key Findings

| Use Case | Monthly Frontier Cost | Monthly Local Cost | Savings |
|---|---|---|---|
| Customer Support Chat | $54,000 | $3,500 | **93%** |
| Document Summarization | $90,000 | $3,500 | **96%** |
| Code Review Assistant | $27,000 | $3,500 | **87%** |
| HR Resume Screening | $75,000 | $4,000 | **95%** |
| Legal Contract Analysis | $120,000 | $4,500 | **96%** |

- **Average cost reduction: 60–96%** when moving high-volume workloads to local GPU infrastructure
- Breakeven typically occurs at **800–2,500 API calls/day** depending on token density
- Local models add **20–40ms latency advantage** for on-prem deployments vs. API round-trips
- Data privacy requirements alone justify local deployment for legal and HR use cases regardless of cost

---

## Project Structure

```
02-genai-cost-model/
├── README.md                  # This file
├── cost_model.ipynb           # Full analysis notebook (4 sections, 4+ charts)
└── decision_framework.md      # 2-page practitioner decision guide
```

---

## Methodology

### Cost Model
- **Frontier API pricing** uses 2024 production rates (GPT-4o, Claude Sonnet)
- **Local infrastructure** modeled on realistic GPU server configs (A100, H100, RTX 4090)
- Monthly costs include: API tokens × price/token, or (server amortization + power + ops labor)
- Token counts estimated from industry benchmarks per use case type

### Scenarios
Each of the five enterprise scenarios specifies:
- Realistic call volume (calls/day or calls/month)
- Token counts per call (input + output, separately)
- Both frontier API cost and local infrastructure cost
- Breakeven call volume
- Annual savings projection

### Decision Framework
A weighted scoring matrix across five dimensions:
1. **Cost efficiency** — pure unit economics
2. **Latency** — p95 response time requirements
3. **Output quality** — task-specific accuracy needs
4. **Data privacy** — regulatory and contractual constraints
5. **Maintenance overhead** — MLOps capacity required

---

## How to Run

### Prerequisites

```bash
pip install pandas matplotlib seaborn numpy jupyter
```

### Launch Notebook

```bash
cd 02-genai-cost-model
jupyter notebook cost_model.ipynb
```

Or with JupyterLab:

```bash
jupyter lab cost_model.ipynb
```

### Run All Cells

Use **Kernel → Restart & Run All** to reproduce all charts and calculations from scratch. No API keys required — all computations are purely mathematical.

---

## Data Sources & Assumptions

| Item | Source / Assumption |
|---|---|
| GPT-4o pricing | OpenAI public pricing page (Nov 2024): $5/1M input, $15/1M output |
| Claude Sonnet pricing | Anthropic public pricing (Nov 2024): $3/1M input, $15/1M output |
| A100 80GB server | AWS p4d.24xlarge equivalent: ~$3,000/month amortized |
| H100 80GB server | Lambda Labs on-demand: ~$4,500/month |
| RTX 4090 workstation | On-prem: ~$2,000/month (amortization + power + colocation) |
| Token counts | Industry benchmarks: support chat ~500 tokens/call, legal docs ~8K tokens/call |
| Latency estimates | Measured medians from public benchmarks and vendor SLAs |

---

## Skills Demonstrated

- **Unit economics modeling** — cost-per-call, breakeven, NPV-style annual savings
- **Infrastructure cost analysis** — CapEx vs. OpEx tradeoffs for GPU compute
- **Decision framework design** — weighted scoring matrices for multi-criteria decisions
- **Data visualization** — matplotlib/seaborn charts for executive and technical audiences
- **AI product strategy** — translating cost data into actionable build-vs-buy recommendations

---

## Author

Built as part of an AI Product Analyst portfolio demonstrating quantitative reasoning and product strategy skills for enterprise GenAI deployments.
