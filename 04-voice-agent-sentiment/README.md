# AI Voice Agent — Support Ops & Sentiment Analytics Engine

A portfolio-grade analytics system for evaluating AI voice agent performance across customer support calls. Analyzes 200 synthetic call transcripts to surface quality metrics, sentiment patterns, failure modes, and escalation triggers — with no external API dependencies.

---

## What the System Does

AI voice agents handle thousands of support calls daily. Without systematic analysis, failure modes go undetected, escalation decisions are inconsistent, and agent quality degrades silently. This system provides:

- **Sentiment scoring** for both customer experience and agent performance across every call
- **Failure mode detection** — identifying agent loops, sentiment misreads, wrong escalations, and incomplete resolutions
- **Escalation threshold optimization** — a sweep across confidence/sentiment thresholds with ROC-style analysis showing that a threshold of 0.4 reduces false-positive escalations by ~35%
- **QA scorecards** across five dimensions (accuracy, empathy, efficiency, resolution, compliance) with bottom-decile flagging for human review
- **Keyword taxonomies** per call category using TF-IDF to understand what customers are actually asking about

---

## Key Metrics Surfaced

| Metric | Description |
|---|---|
| `customer_sentiment` | Normalized score from −1 (hostile) to +1 (satisfied) |
| `agent_performance` | 0–1 composite of response quality and resolution behavior |
| `resolution_confidence` | 0–1 estimate of how confidently the issue was resolved |
| `failure_mode_flags` | Boolean flags: agent_loop, wrong_escalation, sentiment_mismatch, incomplete_resolution, excessive_duration |
| `qa_score` | Aggregate QA score across 5 dimensions (0–100) |
| **Escalation TPR/FPR** | True/false positive rates at each threshold increment |

---

## Architecture Overview

```
data/
  generate_transcripts.py     ← Synthetic data generator (200 calls, 5 categories)
  transcripts.json            ← Generated dataset (auto-created on run)

sentiment_engine.ipynb        ← Main analysis notebook (6 sections)

escalation_framework.md       ← Threshold logic, handoff protocol, KPIs
qa_rubric.md                  ← Scoring rubric for QA dimensions
```

### Analysis Pipeline

```
Raw Transcripts (JSON)
        │
        ▼
Section 1: EDA — distributions, durations, category/outcome splits
        │
        ▼
Section 2: Sentiment Engine — keyword/rule-based scorer per call
        │
        ▼
Section 3: Simulated LLM Summarization — issue, resolution, failure indicators
           + TF-IDF keyword taxonomy per category
        │
        ▼
Section 4: Failure Mode Analysis — 5 failure types, frequency by category,
           correlation matrix
        │
        ▼
Section 5: Escalation Framework — threshold sweep, ROC-like curve,
           human-in-the-loop triggers
        │
        ▼
Section 6: QA Scorecard — 5-dimension scoring, aggregate dashboard,
           bottom-10% flagging
```

---

## How to Run

### 1. Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

### 2. Generate Synthetic Data

```bash
cd 04-voice-agent-sentiment
python data/generate_transcripts.py
```

This creates `data/transcripts.json` with 200 fully structured call transcripts.

### 3. Run the Notebook

```bash
jupyter notebook sentiment_engine.ipynb
```

Run all cells top to bottom. Each section is self-contained with inline explanations.

---

## Failure Modes Modeled

| Failure Mode | Description | Simulated By |
|---|---|---|
| `agent_loop` | Agent repeats the same response 3+ times | Duplicate utterance detection |
| `wrong_escalation` | Call escalated despite high sentiment/confidence | Outcome vs. score mismatch |
| `sentiment_mismatch` | Agent tone diverges from customer emotional state | Polarity divergence scoring |
| `incomplete_resolution` | Call ends without confirming issue resolved | Absence of resolution keywords |
| `excessive_duration` | Call exceeds category-typical duration by >2σ | Duration z-score thresholding |

---

## Portfolio Context

This project demonstrates skills relevant to **AI Product Analytics** roles:
- Designing evaluation frameworks for LLM/AI agent systems
- Translating model behavior into business metrics
- Threshold optimization with precision/recall trade-off analysis
- QA rubric design for human review workflows
- Communicating findings through structured notebook narratives
