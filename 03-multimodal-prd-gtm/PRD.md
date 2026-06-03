# Product Requirements Document
## HireIQ Vision — Multimodal AI Assistant for HR Workflows

---

| Field | Value |
|---|---|
| **Document Version** | 1.4 |
| **Feature Name** | HireIQ Vision |
| **Codename** | Project Lens |
| **Author** | Gowtham Teki, Senior Product Manager |
| **Created** | 2026-01-15 |
| **Last Updated** | 2026-06-03 |
| **Status** | Approved — In Development |
| **Target Launch** | Q3 2026 (General Availability) |
| **Reviewers** | Priya Nair (VP Product), Daniel Osei (Eng Lead), Sofia Marchetti (Design), Raj Iyer (ML Lead), Leah Torres (Legal/Compliance) |
| **Stakeholder Sign-off** | VP Product ✓ | Eng Lead ✓ | Legal ✓ |

---

## Table of Contents

1. Executive Summary
2. Background & Strategic Context
3. Problem Statement
4. User Personas
5. Jobs-to-be-Done
6. Solution Overview
7. Assumptions & Dependencies
8. Functional Requirements — Module A: Image Ingestion & Processing
9. Functional Requirements — Module B: Multimodal Query Interface
10. Functional Requirements — Module C: Resume & Document Intelligence
11. Functional Requirements — Module D: Org Chart & Team Structure Analysis
12. Functional Requirements — Module E: Interview Artifact Processing
13. Functional Requirements — Module F: Context Management & Memory
14. Non-Functional Requirements
15. User Stories
16. Success Metrics & KPIs
17. Out of Scope
18. Edge Cases & Error Handling
19. Technical Constraints & Dependencies
20. Privacy & Compliance
21. Accessibility Requirements
22. Rollout Strategy
23. Open Questions
24. Appendix A — Glossary
25. Appendix B — References & Research

---

## 1. Executive Summary

HireIQ Vision extends the HireIQ platform with multimodal AI capabilities, enabling enterprise HR and recruiting teams to submit both text and image inputs to the AI assistant. Users can upload resume screenshots, photograph whiteboard interview notes, paste org chart images, and share job description scans — receiving structured AI analysis without manual transcription.

The feature addresses a measurable productivity gap: recruiting teams spend an estimated **4.2 hours per week per recruiter** manually transcribing visual information into text-based AI tools, introducing transcription errors and context loss. HireIQ Vision eliminates this gap by integrating vision-capable LLM inference directly into existing recruiting workflows.

**Target outcome:** Reduce recruiter time-on-task for candidate evaluation workflows by 30% within 6 months of GA launch, measured against baseline telemetry.

**Launch approach:** Three-phase rollout — internal alpha (weeks 1–4), closed beta with 15 enterprise design partners (weeks 5–10), general availability (weeks 11–16).

---

## 2. Background & Strategic Context

HireIQ launched in 2022 as an AI-powered ATS and recruiting intelligence platform. The core product handles job requisition management, candidate pipeline tracking, AI-generated interview question suggestions, and recruiter productivity analytics. As of Q1 2026, HireIQ serves 340 enterprise customers, processes approximately 2.4 million candidate applications annually, and has an ARR of $42M.

**Strategic driver:** The HR tech market is consolidating around AI-native platforms. Competitors (Greenhouse, Lever, Ashby) are all investing in AI copilot features. The window for differentiation on multimodal capability is 12–18 months before it becomes table stakes. Internal NPS surveys and customer advisory board sessions (Q4 2025) consistently surfaced document/image handling as the single largest friction point in daily recruiter workflows.

**Technical enabler:** The maturity of commercially available multimodal LLM APIs (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro) as of late 2025 makes this feature buildable at enterprise reliability standards within a 12-week development cycle. The primary engineering investment is in the ingestion pipeline, prompt engineering, and safety/compliance layer — not in training custom vision models.

---

## 3. Problem Statement

### 3.1 The Core Problem

Enterprise recruiting workflows are visually rich but tooling is text-only. The AI tools available to recruiters today — including the existing HireIQ AI assistant — accept only plain text. This forces users to manually transcribe visual information before they can get AI help, creating three compounding problems:

**Problem 1 — Transcription Time Tax**  
Recruiters spend significant time converting visual information to text. Based on a time-diary study with 28 HireIQ users (November 2025):
- Average 18 minutes per complex candidate evaluation session spent on transcription
- 4.2 hours/week per recruiter at median workload (14 candidate evaluations/week)
- Annualized: ~218 hours/recruiter/year on transcription alone

**Problem 2 — Context Loss & Accuracy Degradation**  
Manual transcription introduces errors that compound downstream:
- 67% of users in our survey reported "frequently" omitting details when transcribing resume content
- Org chart relationships and hierarchy are nearly impossible to transcribe accurately without extensive effort
- Whiteboard interview notes lose spatial context (which items were adjacent, circled, crossed out) when converted to linear text

**Problem 3 — Workflow Fragmentation**  
Users currently work across 5–7 different tools in a single candidate evaluation workflow:
- Email (receiving resume PDFs)
- PDF viewer or screenshot tool
- Manual copy-paste or transcription
- HireIQ AI assistant (text only)
- Separate note-taking app for interview artifacts
- Slack for sharing org charts and team context

This fragmentation increases cognitive load, slows decision-making, and reduces the effectiveness of AI assistance.

### 3.2 Quantified Pain Points

| Pain Point | Measurement | Source |
|---|---|---|
| Transcription time per recruiter/week | 4.2 hours | Time-diary study, n=28, Nov 2025 |
| Users who omit details when transcribing | 67% | In-product survey, n=214, Oct 2025 |
| Average tools used per candidate evaluation | 5.7 | Session recording analysis, Sep 2025 |
| Recruiters who have "given up" on AI tools due to format limitations | 31% | Churn risk survey, Dec 2025 |
| Estimated productivity cost per 100-person recruiting team/year | $1.4M | Calculated at $65/hr blended recruiter cost |

### 3.3 Why Now

- Multimodal LLM APIs are production-ready (sub-3s latency, >99% uptime SLAs available)
- Enterprise customers have begun requesting multimodal capability explicitly in procurement conversations (8 enterprise RFPs in Q4 2025 specifically mentioned "image input support")
- A well-funded competitor (Talently AI) announced a multimodal product in January 2026; they are 6–8 months behind HireIQ in enterprise deployment maturity but moving fast

---

## 4. User Personas

### Persona 1: Enterprise Recruiter — "Maya"

**Name:** Maya Chen  
**Role:** Senior Technical Recruiter  
**Company Size:** 3,500 employees, Series D tech company  
**Experience:** 6 years in recruiting, 3 years using AI tools  
**Tech Comfort Level:** High — early adopter, uses AI tools daily, comfortable with browser extensions and integrations

**Day-to-Day Context:**  
Maya manages 12–18 open requisitions simultaneously across engineering and product roles. She reviews 30–50 resumes per day during active sourcing periods, conducts 8–12 initial screens per week, and coordinates with 6–10 hiring managers. She is the primary user who will interact with HireIQ Vision daily.

**Goals:**
- Reduce time from resume receipt to candidate recommendation
- Provide hiring managers with structured, consistent candidate summaries
- Identify relevant experience quickly across diverse resume formats
- Get AI help interpreting technical skills from resume screenshots without re-typing everything

**Frustrations:**
- Resumes arrive as PDFs, images, LinkedIn screenshots, and sometimes photographed paper printouts — none of which the current AI assistant can handle
- Spends 30–45 minutes per week just reformatting content to paste into AI tools
- AI suggestions based on truncated/transcribed content are frequently off-base
- Has to re-explain context for every new conversation; no memory across sessions

**Key Jobs-to-be-Done:**  
"When I receive a resume screenshot or LinkedIn profile export, I want to immediately ask the AI follow-up questions about the candidate without having to retype everything."

---

### Persona 2: Hiring Manager — "David"

**Name:** David Okafor  
**Role:** Director of Engineering  
**Company Size:** 8,000 employees, public enterprise software company  
**Experience:** 12 years in engineering, 4 years in management  
**Tech Comfort Level:** Medium — uses prescribed tools competently, not an early adopter, values reliability over novelty

**Day-to-Day Context:**  
David is involved in 3–5 active searches at any given time. He receives candidate packets prepared by recruiters, participates in debrief sessions, and makes final hire/no-hire decisions. He occasionally uses the AI assistant but relies primarily on recruiter-prepared summaries. His interface with HireIQ Vision will be less frequent but high-stakes.

**Goals:**
- Quickly assess whether a candidate meets technical bar without reading 3-page resumes
- Share org chart screenshots and ask AI to suggest where a candidate would fit
- Get structured summaries of whiteboard interview notes immediately after an interview session
- Reduce the time between interview completion and written feedback submission

**Frustrations:**
- Has to wait for recruiter summaries because the AI can't directly read the candidate materials he has
- Whiteboard interview notes are always lost or unavailable during debrief — no easy capture workflow
- Org chart discussions with AI always require lengthy context-setting

**Key Jobs-to-be-Done:**  
"When I photograph my whiteboard after a technical interview, I want the AI to draft structured interview feedback from the image within 60 seconds."

---

### Persona 3: HR Operations Lead — "Sandra"

**Name:** Sandra Mbeki  
**Role:** HR Operations Lead / HR Systems Administrator  
**Company Size:** 12,000 employees, Fortune 500 manufacturing company  
**Experience:** 15 years in HR, 5 years in HR technology administration  
**Tech Comfort Level:** Medium-Low — prefers configured systems over open-ended tools, risk-averse, compliance-focused

**Day-to-Day Context:**  
Sandra manages the HireIQ deployment for a large enterprise, including user provisioning, integration oversight, compliance reporting, and vendor management. She is the buyer/champion for new HireIQ features, not a daily end-user. She will evaluate HireIQ Vision from a risk, compliance, and ROI perspective before approving rollout.

**Goals:**
- Ensure any AI feature handling employee/candidate data meets GDPR, CCPA, and SOC 2 requirements
- Demonstrate ROI to CHRO with measurable productivity metrics
- Minimize disruption to existing recruiter workflows during rollout
- Maintain audit trail for all AI-assisted decisions (regulatory requirement in EU operations)

**Frustrations:**
- New AI features often launch without adequate documentation of data handling and retention policies
- Hard to explain AI capability to CHRO without concrete, role-specific examples
- Multimodal inputs raise questions about PII in images that the vendor hasn't addressed previously

**Key Jobs-to-be-Done:**  
"When our legal team asks how candidate image data is processed and retained, I want to be able to provide a complete, accurate answer from vendor documentation within 24 hours."

---

## 5. Jobs-to-be-Done

| JTBD ID | When I... | I want to... | So I can... |
|---|---|---|---|
| JTBD-01 | receive a resume as an image or screenshot | upload it directly and ask questions | skip manual transcription |
| JTBD-02 | finish a whiteboard technical interview | photograph the whiteboard and get a structured summary | submit accurate feedback without losing details |
| JTBD-03 | have an org chart screenshot in Slack | paste it into the AI and ask where a candidate fits | make headcount recommendations faster |
| JTBD-04 | see a job description image from a competitor | analyze it against our open roles | understand competitive positioning quickly |
| JTBD-05 | review multiple candidates in one session | maintain context across multiple images and queries | avoid re-explaining background with every question |
| JTBD-06 | manage a large requisition with 200+ applicants | batch-process resume images for initial screening criteria | reduce manual review volume |
| JTBD-07 | need to audit an AI-assisted decision | access a complete log of what images and queries were submitted | satisfy compliance and legal review requirements |
| JTBD-08 | share a candidate summary with a hiring manager | export AI analysis to a structured, shareable format | present candidate recommendations professionally |

---

## 6. Solution Overview

HireIQ Vision adds a multimodal input layer to the existing HireIQ AI assistant. Users can attach images alongside text queries in the assistant chat interface. The system processes image inputs through a vision-capable LLM inference pipeline, extracts structured information, and returns contextually relevant responses that incorporate both the visual content and the user's text query.

**Core Capabilities:**

1. **Image upload and processing** — drag-and-drop or paste images (PNG, JPG, PDF pages, WebP) directly into the assistant interface
2. **Resume intelligence from images** — extract, structure, and analyze candidate information from resume screenshots without OCR preprocessing
3. **Interview artifact analysis** — process whiteboard photos, handwritten notes, and diagram images in the context of interview evaluation
4. **Org chart interpretation** — analyze organizational structure images to answer questions about team composition, reporting relationships, and headcount
5. **Contextual memory within session** — maintain image context across multiple queries within a conversation thread
6. **Audit trail** — log all multimodal interactions for compliance and review purposes

**What Changes for Users:**  
The chat interface gains an image attachment button. Everything else in the UX is unchanged. Users who never use images experience no disruption.

**Technical Approach:**  
Route image-containing queries to a multimodal LLM endpoint (GPT-4o or Claude 3.5 Sonnet, vendor TBD by ML team). Strip, compress, and hash images before transmission. Maintain conversation state in a session context store. Log all interactions to the existing audit log infrastructure.

---

## 7. Assumptions & Dependencies

### Assumptions
- The multimodal LLM API selected will maintain >99.5% uptime SLA — if not, fallback behavior (graceful degradation to text-only) is required
- Enterprise customers will accept that images are processed by a third-party LLM API, subject to data processing agreements (DPAs)
- Image inputs will not exceed 20MB per image and 50MB per session in the vast majority of use cases (based on actual screenshot file size analysis)
- Users have access to camera/phone capability for whiteboard capture — not a safe assumption for all enterprise environments; in-app guidance will address this

### Hard Dependencies
- **Multimodal LLM API:** Contract and DPA must be signed with LLM vendor before beta launch. Currently in procurement review.
- **Image storage infrastructure:** S3-compatible object storage for temporary image retention (30-day default, configurable per customer). Requires infra team sign-off.
- **Audit log schema extension:** Existing audit log must be extended to capture image hash, dimensions, and user attribution. Data team dependency.
- **Enterprise SSO integration:** Image upload permissions must be scoped to user roles via existing RBAC system. No new auth work required — dependency on RBAC team confirming compatibility.

### Soft Dependencies
- Updated DPA templates for enterprise contracts (Legal team, targeting completion 4 weeks before beta)
- Customer-facing data processing FAQ document (Customer Success, targeting completion before beta onboarding)

---

## 8. Functional Requirements — Module A: Image Ingestion & Processing

**FR-001 — Image Upload via Drag-and-Drop**  
The system shall allow users to drag image files (PNG, JPG, JPEG, WebP, PDF) from their desktop into the assistant chat interface and attach them to a query.  
*Priority: P0 | Acceptance: File appears as attachment preview in chat input; supported formats confirmed; unsupported formats show inline error*

**FR-002 — Image Upload via Paste**  
The system shall allow users to paste images from the clipboard (Ctrl+V / Cmd+V) directly into the chat input field.  
*Priority: P0 | Acceptance: Pasted image renders as attachment preview; clipboard images from screenshot tools and browsers are supported*

**FR-003 — Image Upload via File Picker**  
The system shall provide a file attachment button in the chat interface that opens the native OS file picker filtered to supported image/PDF types.  
*Priority: P0 | Acceptance: Clicking button opens file picker; selecting a file attaches it to current query*

**FR-004 — Image Format Validation**  
The system shall validate uploaded images for format compatibility and file size limits before submission. Unsupported formats shall display an inline error message with supported format list.  
*Priority: P0 | Acceptance: Files >20MB show size limit error; unsupported formats show format error; valid files proceed to preview*

**FR-005 — Multi-Image Attachment**  
The system shall support attaching up to 5 images in a single query.  
*Priority: P1 | Acceptance: Up to 5 image thumbnails display in query input; 6th image triggers inline error*

**FR-006 — Image Compression & Optimization**  
The system shall automatically compress images larger than 5MB to a maximum of 5MB before transmission to the LLM API, preserving aspect ratio.  
*Priority: P0 | Acceptance: Images >5MB are compressed server-side; image quality remains sufficient for text extraction (tested against a benchmark image set)*

**FR-007 — PDF Page Extraction**  
The system shall support PDF uploads and automatically extract and process the first 5 pages of a PDF as images.  
*Priority: P1 | Acceptance: PDF upload succeeds; system renders PDF pages as images; user sees page count confirmation; only pages 1–5 are processed with notice if document exceeds 5 pages*

---

## 9. Functional Requirements — Module B: Multimodal Query Interface

**FR-008 — Text + Image Query Submission**  
The system shall allow users to combine a text query with one or more image attachments in a single submission to the AI assistant.  
*Priority: P0 | Acceptance: Combined query reaches the multimodal LLM endpoint with both text and image content; response references visual content where appropriate*

**FR-009 — Image-Only Query Handling**  
The system shall accept queries that contain an image with no accompanying text and automatically prompt the model to describe and analyze the image in the context of recruiting/HR use cases.  
*Priority: P1 | Acceptance: Image-only submission returns a relevant analysis; model does not return "no text provided" errors*

**FR-010 — Response Streaming**  
The system shall stream AI responses token-by-token as they are generated, beginning within 2 seconds of query submission.  
*Priority: P0 | Acceptance: First token appears ≤2s after submission for 95th percentile of requests; streaming renders progressively in the chat UI*

**FR-011 — Contextual Follow-Up Queries**  
The system shall maintain image context within a conversation thread, allowing users to ask follow-up questions that reference previously submitted images without re-uploading.  
*Priority: P0 | Acceptance: Follow-up query "what skills does this candidate have in Python?" correctly references the resume image uploaded 2 turns earlier without re-submission*

**FR-012 — Conversation Thread Management**  
The system shall maintain conversation threads for a minimum of 30 days, allowing users to return to and continue a prior session.  
*Priority: P1 | Acceptance: Users can access threads from the sidebar; conversation history including image references is preserved; images are not re-stored beyond the 30-day retention window*

---

## 10. Functional Requirements — Module C: Resume & Document Intelligence

**FR-013 — Resume Structured Extraction**  
When a resume image is submitted, the system shall extract and return structured candidate information including: name, contact information, work experience (company, title, dates, responsibilities), education, and skills/certifications.  
*Priority: P0 | Acceptance: Structured JSON extraction achieves ≥90% field accuracy on a benchmark set of 100 diverse resume images (established in ML evaluation)*

**FR-014 — Resume Comparison**  
The system shall support uploading multiple resume images in a session and answering comparative questions (e.g., "which of these two candidates has more backend experience?").  
*Priority: P1 | Acceptance: Comparative question referencing two resumes in the same thread returns a differentiated analysis citing specific evidence from each*

**FR-015 — Job Description Image Analysis**  
The system shall accept an image of a job description (screenshot, photograph, or scanned document) and extract role requirements, qualifications, and responsibilities.  
*Priority: P1 | Acceptance: JD image extraction achieves ≥85% requirement capture rate on benchmark test set*

**FR-016 — Resume-to-JD Matching from Images**  
The system shall support submitting a resume image and a job description image together and generating a candidate fit summary with match score.  
*Priority: P1 | Acceptance: Match summary cites specific evidence from both documents; match score is calibrated within ±15% of human rater score on benchmark evaluation*

---

## 11. Functional Requirements — Module D: Org Chart & Team Structure Analysis

**FR-017 — Org Chart Parsing**  
The system shall accept org chart images (screenshots from org chart tools, PowerPoint org charts, whiteboard-drawn hierarchies) and identify reporting relationships, team names, and role titles.  
*Priority: P1 | Acceptance: Org chart parsing correctly identifies direct reports and reporting levels for ≥80% of nodes in benchmark test set of 20 org chart images*

**FR-018 — Headcount Gap Analysis**  
When provided an org chart image and a job description or role description, the system shall suggest where within the org structure a new hire would be placed and what team gaps exist.  
*Priority: P2 | Acceptance: Suggestion includes rationale citing specific org chart context; suggestion is rated "plausible" by 80% of recruiter testers in beta evaluation*

---

## 12. Functional Requirements — Module E: Interview Artifact Processing

**FR-019 — Whiteboard Photo Analysis**  
The system shall accept a photograph of a whiteboard taken after a technical interview and return a structured analysis including: topics discussed (inferred), candidate work visible, and a draft interview notes summary.  
*Priority: P1 | Acceptance: Whiteboard analysis correctly identifies primary technical topic(s) in ≥75% of benchmark cases; draft summary is rated "useful as a starting point" by ≥70% of beta testers*

**FR-020 — Interview Notes Structuring**  
The system shall accept a photograph of handwritten interview notes and return structured, formatted notes suitable for submission as formal interview feedback.  
*Priority: P1 | Acceptance: Handwriting legibility threshold — system shall process notes where handwriting is legible to a human reader; illegible submissions receive a graceful fallback response*

**FR-021 — Interview Scorecard Prefill**  
The system shall optionally auto-populate the HireIQ interview scorecard fields based on whiteboard/notes analysis when the user approves.  
*Priority: P2 | Acceptance: Prefilled fields are clearly marked as AI-generated; user must explicitly confirm before submission; no scorecard field is submitted without user review*

---

## 13. Functional Requirements — Module F: Context Management & Memory

**FR-022 — Session Context Persistence**  
The system shall maintain all images and conversation turns for the duration of a session (defined as continuous activity within a 4-hour window) without requiring re-upload.  
*Priority: P0 | Acceptance: Images submitted at session start are accessible in queries 90 minutes later without re-upload*

**FR-023 — Image Reference in Responses**  
When the AI response references visual content from a submitted image, the system shall indicate which image is being referenced (e.g., "In the resume you uploaded...").  
*Priority: P1 | Acceptance: Responses referencing multi-image sessions correctly attribute information to the correct source image in ≥90% of cases*

**FR-024 — Context Clear / Reset**  
The system shall provide a "Clear context" action that resets the current session, purging image attachments and conversation history.  
*Priority: P0 | Acceptance: Clear action removes all attachments and history from current view; confirmation dialog prevents accidental clears*

**FR-025 — Candidate Record Linking**  
The system shall allow users to optionally associate an image submission with an existing candidate record in HireIQ, linking the conversation to that candidate's profile.  
*Priority: P2 | Acceptance: Linked conversations appear on the candidate record; unlinking removes the association without deleting the conversation*

---

## 14. Non-Functional Requirements

### 14.1 Performance

| Requirement | Target | Measurement |
|---|---|---|
| Time to first token (p50) | ≤1.5 seconds | Server-side telemetry |
| Time to first token (p95) | ≤3.0 seconds | Server-side telemetry |
| Image processing / upload latency (p95) | ≤2.0 seconds | Client-to-server upload complete |
| Full response completion (p50, 200-token response) | ≤8 seconds | End-to-end client measurement |
| Concurrent users supported without degradation | 500 | Load testing benchmark |
| API error rate | <0.5% | 7-day rolling average |

### 14.2 Reliability

- System availability: 99.9% monthly uptime (excluding scheduled maintenance)
- Graceful degradation: if multimodal LLM API is unavailable, text-only queries shall continue functioning; users receive clear notice that image processing is temporarily unavailable
- Image upload failures shall return actionable error messages within 5 seconds

### 14.3 Security

- All images transmitted over TLS 1.3
- Images stored in encrypted object storage (AES-256 at rest)
- Images are not used for model training by the LLM vendor (DPA requirement)
- Image data is isolated per tenant (no cross-customer data access)
- Access to multimodal feature is gated by role-based permissions (admin can enable/disable per user or group)
- All image submissions are logged with user ID, timestamp, and SHA-256 hash of the image

### 14.4 Scalability

- Image processing pipeline shall scale horizontally to handle 10x current load without architectural change
- Per-customer image storage quotas shall be configurable (default: 10GB/month)
- Rate limiting: 100 image submissions per user per day (configurable by admin); 500 per org per hour

### 14.5 Accessibility

- See Section 21 (Accessibility Requirements) for full WCAG 2.1 AA compliance requirements
- Image attachment controls must be keyboard-navigable
- Error messages must be screen-reader compatible
- All image content processed by AI must be representable as text for assistive technology users

---

## 15. User Stories

**US-001** — As a recruiter, I want to drag a resume screenshot into the chat and ask "what are this candidate's top 3 technical skills?" so that I can quickly assess technical fit without reading the full resume.  
*Acceptance Criteria: Image attaches to query; AI response identifies and lists 3 skills with evidence cited from the image; response arrives within 10 seconds*

**US-002** — As a recruiter, I want to paste a copied screenshot from LinkedIn directly into the assistant so that I don't have to save it as a file first.  
*Acceptance Criteria: Ctrl+V in chat input attaches clipboard image; preview displays; query proceeds normally*

**US-003** — As a hiring manager, I want to photograph my whiteboard after a technical interview and get a structured summary of what was discussed so that I can submit interview feedback accurately.  
*Acceptance Criteria: Whiteboard photo accepted; AI returns summary with inferred topics, candidate work visible, and suggested feedback bullet points; user can edit before submitting*

**US-004** — As a recruiter, I want to upload two resume images and ask "which candidate is more qualified for a senior backend role?" so that I can make comparative decisions faster.  
*Acceptance Criteria: Both images accepted in one session; comparative response cites specific evidence from each resume; response is differentiated, not generic*

**US-005** — As an HR operations lead, I want to configure which user roles have access to the image upload feature so that I can control rollout and manage compliance risk.  
*Acceptance Criteria: Admin panel shows multimodal feature toggle by role; changes take effect within 5 minutes; audit log captures configuration changes*

**US-006** — As a recruiter, I want to upload a PDF resume and have the AI analyze the first page without me needing to convert it to an image first.  
*Acceptance Criteria: PDF upload accepted; system extracts first page as image; AI analyzes content; user is notified if document exceeds 5 pages*

**US-007** — As a hiring manager, I want to share an org chart screenshot and ask "where would a senior ML engineer fit in this team?" so that I can frame headcount requests accurately.  
*Acceptance Criteria: Org chart image accepted; AI identifies relevant team/role and provides a placement suggestion with rationale*

**US-008** — As a recruiter, I want my image uploads to be retained in the conversation thread so that I can return to a candidate evaluation session the next day without re-uploading everything.  
*Acceptance Criteria: Conversation thread persists for 30 days; images are accessible in prior threads up to retention limit; images beyond retention window show expired notice*

**US-009** — As a recruiter, I want to see a clear error message when I try to upload an unsupported file type so that I know what formats are accepted.  
*Acceptance Criteria: Unsupported file upload shows inline error with list of supported formats; does not submit query; no page reload*

**US-010** — As an HR operations lead, I want all AI interactions involving image uploads to appear in the audit log with user attribution so that I can satisfy compliance review requests.  
*Acceptance Criteria: Audit log entry captures user ID, timestamp, image hash, query text (truncated), and response token count for every multimodal interaction*

**US-011** — As a recruiter, I want to ask a follow-up question about a resume I uploaded three turns ago without re-uploading it so that the conversation flows naturally.  
*Acceptance Criteria: Follow-up query in same thread correctly references prior image; AI response demonstrates awareness of image content without user re-submitting*

**US-012** — As a recruiter, I want to clear my current session context so that a new candidate evaluation starts fresh without prior context contaminating responses.  
*Acceptance Criteria: Clear context button appears in session; confirmation dialog prevents accidental clear; after confirmation, new query has no prior context*

**US-013** — As a hiring manager, I want the AI to prefill my interview scorecard from whiteboard notes I photographed so that I can save time on documentation.  
*Acceptance Criteria: Prefill option appears after whiteboard analysis; all prefilled fields are visibly marked "AI-suggested"; user must explicitly click confirm before any field is saved to the scorecard*

**US-014** — As a recruiter, I want to link an image analysis session to a specific candidate record in HireIQ so that I can find the analysis easily from the candidate profile.  
*Acceptance Criteria: Link to candidate option appears in session; selecting a candidate associates the conversation with their profile; conversation appears in the candidate's activity timeline*

**US-015** — As an enterprise customer on EU data residency, I want assurance that candidate image data processed by the AI does not leave EU infrastructure so that I can comply with GDPR data localization requirements.  
*Acceptance Criteria: EU data residency configuration routes image processing to EU-hosted LLM endpoint; documentation available confirming EU residency; this is confirmed in DPA*

**US-016** — As a recruiter using a screen reader, I want to be able to attach images to queries using only keyboard navigation so that the feature is accessible to me.  
*Acceptance Criteria: Image attachment button is keyboard focusable and activatable; file selection proceeds via OS keyboard-accessible file picker; attachment confirmation announced by screen reader*

**US-017** — As a recruiter, I want to see a processing indicator while the AI analyzes my image so that I know the system is working and haven't lost my query.  
*Acceptance Criteria: Loading state appears immediately after query submission; first streamed token replaces loading state; loading state is visually distinct from idle and error states*

---

## 16. Success Metrics & KPIs

### 16.1 Primary Metrics (Decision-driving)

| Metric | Baseline | Target (6 months post-GA) | Measurement Method |
|---|---|---|---|
| Recruiter time-on-task for candidate evaluation (minutes) | 24.3 min/evaluation | ≤17 min/evaluation (−30%) | In-app session timing |
| Multimodal feature adoption (% of active users who submit ≥1 image/week) | 0% | ≥45% of active recruiters | Feature telemetry |
| Image query success rate (queries that receive a useful AI response, rated by user) | N/A | ≥78% thumbs-up rate | In-app feedback widget |

### 16.2 Secondary Metrics (Health indicators)

| Metric | Target | Measurement Method |
|---|---|---|
| Image upload success rate | ≥98.5% | Server-side upload logs |
| Time to first token (p95) | ≤3.0 seconds | Server telemetry |
| Feature NPS (multimodal-specific) | ≥40 | Quarterly in-app survey |
| Audit log completeness | 100% of multimodal interactions logged | Automated reconciliation |
| Whiteboard analysis "useful" rating | ≥70% positive | Beta feedback survey |
| Resume extraction accuracy | ≥90% field accuracy | ML evaluation benchmark |

### 16.3 Guardrail Metrics (Must not degrade)

| Metric | Threshold | Action if Breached |
|---|---|---|
| Overall platform NPS | Must not drop >5 points vs. pre-launch baseline | Pause new feature rollout; root cause investigation |
| Text-only query latency | Must not increase by >200ms p95 | Rollback image processing pipeline changes |
| Platform error rate | Must not exceed 1% (from current 0.3%) | Incident response, feature flag to disable image processing |
| Customer churn rate | Must not increase by >0.5pp in 90-day cohort | Customer success escalation, executive review |
| Data breach / privacy incident | Zero tolerance | Immediate feature disable, incident response protocol |

### 16.4 Metric Review Cadence

- **Weekly (during beta):** Adoption, error rate, latency — shared in weekly beta review meeting
- **Bi-weekly (first 90 days post-GA):** All primary and secondary metrics — shared in PM/Eng sync
- **Monthly (steady state):** Full dashboard review including guardrail trends — shared with VP Product and GTM leads
- **Quarterly:** Feature NPS survey, customer advisory board feedback synthesis

---

## 17. Out of Scope

The following are explicitly excluded from this release (v1.4 / Q3 2026 GA):

1. **Video input** — Processing recorded interview videos or screen recordings is out of scope. A future phase may address video.
2. **Real-time camera capture** — In-app camera activation (mobile or desktop) is not supported. Users must capture images externally and upload.
3. **Custom vision model training** — All image processing uses third-party multimodal LLM APIs. Fine-tuning or training proprietary vision models is not in scope.
4. **Batch processing API** — Programmatic bulk image upload via API for integration with external systems is a v2 feature.
5. **Image annotation / markup** — Users cannot draw on or annotate images within the application.
6. **Voice/audio input** — Multimodal does not include audio in this release.
7. **Resume parsing for ATS import** — Image-based resume extraction does not auto-populate ATS candidate records without user review and confirmation (see FR-021 for the scorecard prefill model that does require confirmation).
8. **Automatic PII redaction** — The system will not automatically detect and redact PII from image content before AI processing. Users are advised by in-product guidance to be mindful of sensitive data.
9. **Non-English language OCR optimization** — The feature is launched in English only; multilingual resume/document support is a v1.1 planned feature.
10. **Mobile native app** — HireIQ Vision launches on the web platform only; mobile app support is scheduled for Q4 2026.

---

## 18. Edge Cases & Error Handling

**EC-001 — Completely Blank or Solid-Color Image**  
*Scenario:* User uploads an image that is blank, completely black, or a single solid color.  
*Handling:* Model returns a response indicating no content was detected in the image; suggests user re-upload a different image. Does not return an error state or crash.

**EC-002 — Image Contains Only a Company Logo or Decorative Art**  
*Scenario:* User accidentally uploads a logo or non-document image.  
*Handling:* AI response acknowledges the image content and clarifies that no recruiting-relevant information was found; prompts user to confirm intent or upload a different image.

**EC-003 — Extremely Low Resolution or Blurry Image**  
*Scenario:* User uploads a photo of a resume taken in low light, out of focus, or heavily compressed.  
*Handling:* System attempts processing; if confidence in extracted text is below threshold, AI response includes a quality warning: "The image quality may be affecting accuracy. For best results, ensure the document is well-lit and in focus." Partial results are still returned rather than failing completely.

**EC-004 — Image Contains Personal Sensitive Information (PHI, Financial Data)**  
*Scenario:* User uploads an image containing obvious medical records, financial statements, or other non-recruiting-relevant sensitive data.  
*Handling:* System does not block this at the ingestion layer (would require PII classification that is out of scope). In-product guidance at upload time advises users not to upload non-recruiting data. Audit log records the submission.

**EC-005 — Multi-Language Resume**  
*Scenario:* User uploads a resume with content in a non-English language (e.g., Spanish, Mandarin, Arabic).  
*Handling:* System processes the image; model returns response in English noting that the resume contains non-English content. Extraction quality may be degraded; user is notified. This is known limitation in v1.0.

**EC-006 — Rotated or Upside-Down Image**  
*Scenario:* User uploads a resume photograph that is rotated 90° or 180°.  
*Handling:* Image preprocessing layer applies automatic rotation correction using EXIF orientation data. If rotation correction fails, AI still attempts to process and notes any orientation issue in response.

**EC-007 — LLM API Timeout**  
*Scenario:* The multimodal LLM API does not return a response within the configured timeout (30 seconds).  
*Handling:* System displays an error: "The AI is taking longer than expected. Your image was received — please try again." Retry with exponential backoff is attempted once automatically before surfacing the error. Session context is preserved so user does not lose prior images.

**EC-008 — LLM API Returns Inappropriate Content**  
*Scenario:* AI response contains content that violates content policy (offensive, discriminatory, factually harmful).  
*Handling:* Output filtering layer screens responses before display. Filtered responses return a generic error message. Incident is logged for review. Policy violations are reported to the ML safety team.

**EC-009 — User Uploads Same Image Multiple Times in One Session**  
*Scenario:* User re-uploads the same resume image in the same conversation thread.  
*Handling:* System detects duplicate via SHA-256 hash comparison and displays a notice: "This image has already been uploaded in this conversation. You can reference it in your next question without re-uploading." Image is not re-stored; prior reference is used.

**EC-010 — Image Upload Exceeds Per-Day Rate Limit**  
*Scenario:* A user has submitted 100 images in a single day (default rate limit) and attempts to upload more.  
*Handling:* Upload is rejected with a clear inline message: "Daily image upload limit reached (100 images). Your limit resets at midnight UTC. Contact your admin to request a higher limit." Text-only queries continue functioning normally.

**EC-011 — Session Expires Mid-Conversation**  
*Scenario:* User leaves a conversation open for more than 4 hours (session timeout) and tries to submit a follow-up query referencing images from earlier in the session.  
*Handling:* System prompts user to re-authenticate session. After authentication, prior conversation text history is restored but image context is cleared; user is notified and can re-upload images if needed.

**EC-012 — PDF With Password Protection**  
*Scenario:* User uploads a password-protected PDF.  
*Handling:* System detects encrypted PDF at ingestion and returns an inline error: "This PDF is password-protected and cannot be processed. Please remove the password protection and re-upload." No processing attempt is made.

---

## 19. Technical Constraints & Dependencies

### 19.1 LLM API Constraints

- Maximum image dimensions: 2048×2048 pixels (images larger than this are downscaled before API submission)
- Maximum tokens per multimodal request: 4,096 input tokens (text + image token budget); images consume approximately 765–1085 tokens depending on resolution
- Context window management: sessions approaching token budget limits will require conversation summarization to maintain context without exceeding API limits
- Vendor lock risk: initial release is built on GPT-4o; ML team has validated Claude 3.5 Sonnet as a functional alternative; architecture must allow vendor switching within 2-week sprint

### 19.2 Infrastructure Constraints

- Image storage: S3-compatible object storage; images are retained for 30 days by default, then permanently deleted (configurable to 7 days for customers with stricter retention policies)
- No GPU inference in our infrastructure — all vision processing is outsourced to LLM API vendor
- CDN for image delivery to LLM API — images must be accessible via signed URL for API submission; no direct file upload to LLM API is supported in current architecture

### 19.3 Platform Constraints

- Web browser support: Chrome 100+, Firefox 100+, Safari 15+, Edge 100+ (image paste may not function in older Safari versions — known limitation)
- Mobile web: supported but not optimized; mobile native app support is out of scope for this release
- Maximum conversation thread size: 100 turns (existing limit); multimodal conversations may hit this limit faster due to image token overhead

---

## 20. Privacy & Compliance

### 20.1 Data Classification

Images submitted by users are classified as **Sensitive — Candidate PII** under HireIQ's data classification policy. This classification implies:
- Encrypted in transit (TLS 1.3) and at rest (AES-256)
- Access restricted to submitting user and tenant admins
- Retained for 30 days maximum (configurable to 7 days)
- Included in data export and deletion requests (GDPR Article 17)
- Not used for model training or product analytics

### 20.2 GDPR Considerations

- **Lawful basis for processing:** Images containing candidate PII are processed on the basis of legitimate interest (recruiting workflow) with appropriate safeguards. Customers are responsible for ensuring their use of the feature is consistent with their candidate consent policies.
- **Data Subject Access Requests (DSAR):** The image audit log, including image hashes, will be included in DSAR responses. Actual image files are included in data export requests.
- **Right to Erasure:** Image deletion requests will be honored within 72 hours. Images are permanently deleted from object storage; deletion is confirmed in the audit log.
- **Data Residency:** EU customers on our Enterprise tier can elect EU data residency, which routes all image processing to EU-hosted LLM API endpoints and stores images in EU-region object storage.
- **DPA:** Updated DPA covering image data processing must be signed with LLM API vendor and made available to enterprise customers before beta launch.

### 20.3 SOC 2 Type II Considerations

- Image upload and processing events are logged to the immutable audit log (existing SOC 2 control)
- Access controls on image storage are enforced via existing IAM policies (mapped to SOC 2 CC6.x)
- Image retention and deletion procedures are documented and enforced automatically (mapped to SOC 2 A1.x)
- Penetration testing scope will be expanded to include image upload endpoints before GA

### 20.4 CCPA Considerations

- Candidate images that are submitted in the context of recruiting are "personal information" under CCPA. Customers (as businesses) are responsible for compliance with CCPA consumer rights requests. HireIQ's service agreement already covers this framework; image data is added to the defined categories in the updated privacy policy.

### 20.5 Equal Employment Opportunity (EEO) Considerations

- The system processes resume images and may extract information that is legally protected under EEO law (age indicators, names suggesting ethnicity, photos on resumes common in some international formats).
- Product guidance will advise users not to use visual information for protected-characteristic inference.
- The AI is instructed via system prompt not to comment on or infer protected characteristics from images.
- A "potential EEO risk" indicator will be shown if the model detects that a submitted image may contain a candidate photo (a common resume format in some regions).

---

## 21. Accessibility Requirements

HireIQ Vision must meet **WCAG 2.1 Level AA** compliance for all new UI components.

**Keyboard Navigation**
- Image attachment button: focusable, activatable via Enter/Space
- Drag-and-drop zone: keyboard-accessible via button alternative (FR-003)
- File picker: uses native OS file picker which is inherently accessible
- Clear context button: keyboard focusable; confirmation dialog is keyboard navigable
- All chat interface interactions navigable via Tab key order

**Screen Reader Compatibility**
- Image attachment previews: alt text rendered as "[Filename] — image attached"
- Upload progress states: announced via ARIA live region
- Error messages: rendered in ARIA alert role for immediate announcement
- AI response streaming: content updates announced via ARIA live region (polite)

**Visual Design**
- All new UI controls meet 4.5:1 contrast ratio requirement
- Loading/processing states use both color and non-color indicators (spinner + text)
- Error states use both color (red) and icon (warning symbol) for color-blind users

**Cognitive Accessibility**
- Error messages are written in plain language (<Grade 8 reading level)
- Processing time indicator prevents user confusion during AI response generation
- Session context clear confirmation dialog uses explicit action language ("Clear all images and conversation history")

---

## 22. Rollout Strategy

### Phase 1: Internal Alpha (Weeks 1–4)

**Objective:** Validate core functionality, surface critical bugs, and establish performance baselines in a controlled environment.

**Audience:** HireIQ employees in recruiting and HR roles (estimated 12 users). Engineering team using dogfood accounts.

**Scope:** All functional requirements FR-001 through FR-016 (core ingestion and resume intelligence). FR-017 through FR-025 in limited testing.

**Exit Criteria:**
- Zero P0 bugs open
- Image upload success rate ≥97%
- Time to first token p95 ≤4s (relaxed for alpha)
- All internal testers have submitted feedback; critical usability issues resolved

### Phase 2: Closed Beta (Weeks 5–10)

**Objective:** Validate product-market fit, collect quantitative and qualitative feedback from representative enterprise users, and prepare for GA.

**Audience:** 15 enterprise design partner accounts (selected per criteria in GTM Strategy). Maximum 3 users per account = ~45 beta users.

**Scope:** Full feature set. FR-021 (scorecard prefill) enabled for willing accounts.

**Exit Criteria:**
- Image query success rate (user-rated thumbs-up) ≥75%
- Zero P0 and P1 bugs open
- Time to first token p95 ≤3s
- Net Promoter Score from beta users ≥35
- All compliance documentation reviewed and approved by Legal
- DPA with LLM vendor signed

### Phase 3: General Availability (Weeks 11–16)

**Objective:** Full customer rollout with monitoring, self-serve onboarding, and support readiness.

**Audience:** All HireIQ Enterprise and Growth tier customers (feature-gated; Standard tier excluded in v1.0).

**Rollout Cadence:**
- Week 11: Enable for 10% of eligible customers (canary)
- Week 12: Enable for 25% if canary metrics healthy
- Week 13: Enable for 50%
- Week 14: Enable for 100%
- Weeks 15–16: Monitor, iterate, address GA feedback

**Exit Criteria (Full GA):**
- All Tier 1 and Tier 2 customer support staff trained on multimodal feature
- Help center documentation live
- In-product onboarding tour live
- Monitoring dashboards live with alerting configured

---

## 23. Open Questions

| ID | Question | Owner | Target Resolution |
|---|---|---|---|
| OQ-01 | Which LLM vendor (GPT-4o vs. Claude 3.5 Sonnet) for initial release? Final decision on latency benchmarks and DPA terms. | ML Lead (Raj Iyer) | Week 2 of alpha |
| OQ-02 | What is the right default image retention period — 7 days or 30 days? Customer survey data shows split preference. | PM + Legal | Week 3 of alpha |
| OQ-03 | Should image analysis be included in standard tier pricing or gated to Enterprise/Growth tiers only? | VP Product + Finance | GTM review, week 4 |
| OQ-04 | How do we handle candidates who have submitted photos on resumes (common in EU/Asia)? Does the system comment on the photo? Need explicit system prompt guidance reviewed by Legal. | PM + Legal + ML | Week 2 |
| OQ-05 | EU data residency routing: can we guarantee same API response times from EU LLM endpoints? Need vendor confirmation. | ML Lead + Infra | Week 1 |
| OQ-06 | Rate limit thresholds — 100 images/user/day sufficient? Need usage modeling from beta data. | PM + Data | Post-beta review |

---

## 24. Appendix A — Glossary

| Term | Definition |
|---|---|
| **ATS** | Applicant Tracking System — software for managing recruiting workflows and candidate pipelines |
| **Multimodal AI** | AI systems that can process and reason across multiple input types (text, image, audio, video) |
| **LLM** | Large Language Model — the class of AI model underlying the AI assistant |
| **OCR** | Optical Character Recognition — technology for extracting text from images; in this context, the multimodal LLM performs implicit OCR as part of its reasoning |
| **Vision-capable LLM** | An LLM that accepts image inputs alongside text, processing both in the same inference pass |
| **Tokenization** | The process of converting input (text or image) into numerical representations for LLM processing; images consume token budget |
| **JTBD** | Jobs-to-be-Done — a framework for understanding user motivation in terms of the underlying job a user is trying to accomplish |
| **ICP** | Ideal Customer Profile — the description of the customer type most likely to buy and benefit from the product |
| **DPA** | Data Processing Agreement — a contractual document specifying how a vendor processes customer data under GDPR |
| **SOC 2** | Service Organization Control 2 — an audit framework for data security and availability, widely required by enterprise buyers |
| **GDPR** | General Data Protection Regulation — EU data privacy regulation |
| **CCPA** | California Consumer Privacy Act — California data privacy regulation |
| **RBAC** | Role-Based Access Control — system for controlling feature access based on user roles |
| **P0 / P1 / P2** | Bug/requirement priority levels: P0 = launch blocker, P1 = must-have before GA, P2 = important but deferrable |

---

## 25. Appendix B — References & Research

1. Internal time-diary study: "Recruiter Workflow Inefficiencies — AI Tool Usage Patterns" (HireIQ User Research, November 2025, n=28)
2. Internal survey: "AI Tool Limitations — Recruiter Feedback" (HireIQ Product Analytics, October 2025, n=214)
3. Internal session recording analysis: "Multi-tool Workflow Fragmentation in Enterprise Recruiting" (HireIQ Data Science, September 2025)
4. Customer advisory board session notes: Q4 2025 (available in Notion — restricted to internal PM team)
5. Competitor analysis: Greenhouse AI Copilot, Lever Intelligence, Ashby AI Features (PM research, December 2025)
6. Technical evaluation: GPT-4o vs. Claude 3.5 Sonnet for recruiting document intelligence (ML Team, January 2026)
7. GDPR guidance: Article 17 (Right to Erasure), Article 6 (Lawful Basis for Processing), Recital 47 (Legitimate Interests)
8. EEOC guidance on AI in hiring: "Artificial Intelligence and Algorithmic Fairness" (U.S. EEOC, 2023)
