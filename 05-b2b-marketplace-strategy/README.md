# B2B AI Agent Marketplace — Opportunity Assessment

> **An end-to-end market sizing, competitive analysis, and go-to-market strategy for entering the $12.2B B2B AI agent marketplace by 2027.**

---

## Market Thesis

Enterprise software is undergoing its most significant architectural shift since SaaS. The transition from single-purpose AI features (copilots, classifiers) to **autonomous, multi-step AI agents** capable of executing complete business workflows creates a new category of infrastructure. B2B buyers are not just purchasing software licenses — they are acquiring digital labor.

We estimate the addressable market for verticalized B2B AI agents across HR, Sales, Customer Support, and Legal will reach **$12.2B by 2027**, driven by:

- **Horizontal AI commoditization:** Foundation model costs are falling 10x every 18 months (OpenAI, Anthropic), collapsing the barrier to building domain-aware agents.
- **Enterprise workflow digitization:** Post-pandemic IT spend shifted toward automation; CFOs are willing to pay for measurable headcount-equivalent ROI.
- **Vertical specialization premium:** Generic LLMs have 40-60% task completion rates on complex enterprise workflows; fine-tuned vertical agents exceed 80%.
- **Platform consolidation pressure:** ATS, CRM, and ticketing vendors face displacement from full-stack agent vendors, creating urgency to partner or acquire.

---

## Project Structure

```
05-b2b-marketplace-strategy/
├── README.md                   ← You are here — thesis and navigation guide
├── market_sizing.ipynb         ← Quantitative analysis: TAM/SAM/SOM, comp map, build-buy-partner
├── competitive_analysis.md     ← Deep-dive profiles of 12 competitors + white space analysis
└── strategy_memo.md            ← 12-page consulting-style strategy memo with recommendations
```

---

## Key Findings

| Metric | Value |
|--------|-------|
| Total TAM (2027) | **$12.2B** |
| Highest-opportunity vertical | **Sales AI agents ($4.1B)** |
| Most defensible entry point | **HR + Recruiting agents** |
| Recommended entry strategy | **Partner-first with ATS/CRM platforms** |
| Time to $10M ARR (SOM) | **18 months** with partner distribution |
| Primary competitive threat | **Salesforce Agentforce, ServiceNow AI** |

---

## Methodology

### Market Sizing (Bottom-Up)
The TAM model uses a **segmented company count × adoption rate × ACV** framework:

1. **Universe:** U.S. company counts by size tier (SMB <100, Mid-Market 100-999, Enterprise 1000+) from U.S. Census Business Patterns data.
2. **Vertical scoping:** Each vertical (HR, Sales, Support, Legal) is scoped to the subset of companies with active teams in that function.
3. **Adoption forecasts:** Adoption curves derived from Gartner Hype Cycle data, CBI Insights AI adoption surveys, and analogous SaaS S-curves (e.g., CRM adoption 2005-2012).
4. **ACV benchmarks:** Contract values sourced from disclosed pricing, SEC filings (HireVue, Outreach), and investor decks for comparable verticalized AI vendors.

### Competitive Analysis
12 competitors scored across 5 dimensions: product completeness, enterprise readiness, AI sophistication, pricing competitiveness, and market presence. Scores are based on public product documentation, G2/Gartner peer reviews, job posting analysis, and patent filings.

### Build-Buy-Partner Framework
Decision matrix with 6 weighted criteria evaluated across 3 strategic scenarios. Weights derived from a hypothetical Series B company with $40M in capital, 60-person team, and 18-month runway objective.

---

## How to Run the Notebook

```bash
# Install dependencies
pip install pandas matplotlib seaborn numpy jupyter

# Launch
jupyter notebook market_sizing.ipynb
```

All cells are designed to run sequentially. The notebook is self-contained — no external data files required.

---

## About This Project

This analysis was built as part of an AI Product Analyst portfolio to demonstrate:
- **Quantitative market analysis** (TAM/SAM/SOM modeling)
- **Competitive intelligence synthesis**
- **Strategic decision frameworks** (build-buy-partner)
- **Data visualization** for executive communication
- **Consulting-grade written communication**

---

*Data sources and assumptions detailed in `strategy_memo.md` Appendix.*
