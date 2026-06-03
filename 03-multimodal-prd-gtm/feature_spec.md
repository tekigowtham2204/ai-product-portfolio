# Technical Feature Specification
## HireIQ Vision — Multimodal AI Image Processing

---

| Field | Value |
|---|---|
| **Document Version** | 1.3 |
| **Feature** | HireIQ Vision — Multimodal Input Pipeline |
| **Author** | Gowtham Teki, Senior Product Manager |
| **Technical Review** | Daniel Osei (Eng Lead), Raj Iyer (ML Lead), Alex Park (Infra) |
| **Created** | 2026-02-20 |
| **Last Updated** | 2026-06-03 |
| **Status** | Approved for Implementation |

---

## Table of Contents

1. Overview & Scope
2. System Architecture
3. API Design
4. Data Flow
5. Model Integration Points
6. Latency Budgets
7. Storage & Retention
8. Error States & Handling
9. Security Considerations
10. Observability & Monitoring
11. Testing Strategy

---

## 1. Overview & Scope

This document specifies the technical design for the image processing pipeline, API contracts, model integration, and error handling behavior of HireIQ Vision. It is intended for backend engineers, ML engineers, and infrastructure engineers implementing the feature, and serves as the source of truth for integration decisions.

**Scope of this document:**
- Image ingestion API (upload, validate, store)
- Multimodal query API (text + image to LLM)
- Session context management
- LLM API integration abstraction layer
- Latency budgets per component
- Error state taxonomy and client behavior

**Not in scope of this document:**
- Frontend component design (see Figma spec, linked in Notion)
- LLM prompt engineering and evaluation (see ML team's Model Evaluation doc)
- RBAC configuration and permissions UI (see Platform RBAC spec)

---

## 2. System Architecture

### 2.1 High-Level Component Diagram

```
Client (Browser)
       │
       │ HTTPS / WebSocket
       ▼
┌─────────────────────────────┐
│     API Gateway             │
│  (Auth, Rate Limiting,      │
│   Request Routing)          │
└────────────┬────────────────┘
             │
     ┌───────┴────────┐
     │                │
     ▼                ▼
┌──────────┐    ┌──────────────────────┐
│  Image   │    │  Multimodal Query    │
│ Ingestion│    │  Service             │
│ Service  │    │  (Query orchestrator)│
└────┬─────┘    └──────────┬───────────┘
     │                     │
     ▼                     ▼
┌──────────┐    ┌──────────────────────┐
│  Object  │    │  LLM Abstraction     │
│  Storage │    │  Layer               │
│  (S3)    │    │  (Vendor-agnostic)   │
└──────────┘    └──────────┬───────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
     ┌────────────────┐     ┌──────────────────┐
     │  GPT-4o API    │     │  Claude 3.5      │
     │  (primary)     │     │  Sonnet API      │
     └────────────────┘     │  (failover)      │
                            └──────────────────┘
```

### 2.2 Service Responsibilities

**Image Ingestion Service**
- Accept image uploads from authenticated clients
- Validate format, size, and content type
- Compress images exceeding 5MB
- Generate SHA-256 hash for deduplication and audit
- Store processed image to object storage
- Return a signed, time-limited access URL for use in LLM API calls
- Write ingestion event to audit log

**Multimodal Query Service**
- Accept combined text + image reference(s) queries
- Retrieve image signed URLs from session context
- Construct multimodal request payload
- Call LLM via abstraction layer
- Stream response tokens back to client
- Write query and response metadata to audit log
- Manage session context state

**LLM Abstraction Layer**
- Present a unified API interface regardless of underlying vendor
- Route requests to primary vendor (GPT-4o) with automatic failover to secondary (Claude 3.5 Sonnet)
- Handle vendor-specific request/response format translation
- Enforce token budget limits and context window management
- Wrap vendor errors in standardized error codes

**Session Context Store**
- Persist conversation turns (text + image references) within a session
- Enforce session timeout (4-hour inactivity window)
- Support thread persistence for 30-day retrieval
- Enforce token budget tracking per session

---

## 3. API Design

### 3.1 Image Upload Endpoint

```
POST /api/v1/vision/images
Authorization: Bearer {user_jwt}
Content-Type: multipart/form-data

Body:
  file: <binary image data>
  session_id: string (optional — associates with existing session)
  candidate_id: string (optional — links to candidate record)
```

**Response (201 Created):**
```json
{
  "image_id": "img_01HXYZ789ABCDEF",
  "session_id": "sess_01HABC123DEF456",
  "filename": "resume_jane_doe.png",
  "content_type": "image/png",
  "size_bytes": 1843200,
  "compressed": false,
  "sha256": "a1b2c3d4e5f6...",
  "expires_at": "2026-06-04T14:30:00Z",
  "created_at": "2026-06-03T14:30:00Z"
}
```

**Response (400 Bad Request — unsupported format):**
```json
{
  "error": "UNSUPPORTED_FORMAT",
  "message": "File type 'image/bmp' is not supported. Supported types: image/png, image/jpeg, image/webp, application/pdf",
  "supported_formats": ["image/png", "image/jpeg", "image/webp", "application/pdf"]
}
```

**Response (413 Payload Too Large):**
```json
{
  "error": "FILE_TOO_LARGE",
  "message": "File size 22MB exceeds the maximum allowed size of 20MB.",
  "max_size_bytes": 20971520
}
```

---

### 3.2 Multimodal Query Endpoint

```
POST /api/v1/vision/query
Authorization: Bearer {user_jwt}
Content-Type: application/json

Body:
{
  "session_id": "sess_01HABC123DEF456",
  "query": "What are this candidate's top 3 technical skills?",
  "image_ids": ["img_01HXYZ789ABCDEF"],
  "stream": true,
  "context": {
    "use_case": "resume_analysis",    // hint for system prompt selection
    "job_req_id": "req_01HDEF789"     // optional — for context injection
  }
}
```

**Response (200 OK — streaming, text/event-stream):**
```
data: {"type": "token", "content": "Based"}
data: {"type": "token", "content": " on"}
data: {"type": "token", "content": " the"}
data: {"type": "token", "content": " resume"}
...
data: {"type": "done", "usage": {"input_tokens": 842, "output_tokens": 187}, "response_id": "resp_01HGHI456JKL"}
```

**Response (200 OK — non-streaming):**
```json
{
  "response_id": "resp_01HGHI456JKL",
  "session_id": "sess_01HABC123DEF456",
  "content": "Based on the resume image, this candidate's top 3 technical skills are: (1) Python — demonstrated across 4 roles spanning 7 years, including ML pipeline development and data engineering... (2) ...",
  "model": "gpt-4o-2025-11",
  "usage": {
    "input_tokens": 842,
    "output_tokens": 187,
    "image_tokens": 765
  },
  "images_referenced": ["img_01HXYZ789ABCDEF"],
  "created_at": "2026-06-03T14:31:02Z"
}
```

---

### 3.3 Session Retrieval Endpoint

```
GET /api/v1/vision/sessions/{session_id}
Authorization: Bearer {user_jwt}
```

**Response (200 OK):**
```json
{
  "session_id": "sess_01HABC123DEF456",
  "created_at": "2026-06-03T14:30:00Z",
  "last_activity_at": "2026-06-03T15:45:00Z",
  "expires_at": "2026-06-03T19:45:00Z",
  "turn_count": 6,
  "token_count": 4821,
  "token_budget": 8192,
  "images": [
    {
      "image_id": "img_01HXYZ789ABCDEF",
      "filename": "resume_jane_doe.png",
      "uploaded_at": "2026-06-03T14:30:00Z",
      "available": true
    }
  ],
  "candidate_id": null,
  "turns": [
    {
      "turn_id": "turn_01",
      "role": "user",
      "content": "What are this candidate's top 3 technical skills?",
      "image_ids": ["img_01HXYZ789ABCDEF"],
      "created_at": "2026-06-03T14:31:00Z"
    },
    {
      "turn_id": "turn_02",
      "role": "assistant",
      "content": "Based on the resume image...",
      "created_at": "2026-06-03T14:31:03Z"
    }
  ]
}
```

---

### 3.4 Image Deletion Endpoint

```
DELETE /api/v1/vision/images/{image_id}
Authorization: Bearer {user_jwt}
```

**Response (204 No Content)** — Image deleted, audit log entry written.

**Response (404 Not Found)** — Image ID not found or not accessible to the requesting user.

---

### 3.5 Session Context Clear Endpoint

```
DELETE /api/v1/vision/sessions/{session_id}/context
Authorization: Bearer {user_jwt}
```

**Response (200 OK):**
```json
{
  "session_id": "sess_01HABC123DEF456",
  "status": "context_cleared",
  "images_deleted": 2,
  "turns_cleared": 6
}
```

---

## 4. Data Flow

### 4.1 Image Upload Flow

```
1. Client → API Gateway
   - JWT validation
   - Rate limit check (100 images/user/day)
   - Request size validation (≤20MB)

2. API Gateway → Image Ingestion Service
   - Format validation (MIME type whitelist)
   - File size check (reject if >20MB)
   - Compute SHA-256 hash

3. Deduplication check
   - Query session context: does this hash already exist in this session?
   - If duplicate: return existing image_id with duplicate notice
   - If not duplicate: continue

4. Compression (if needed)
   - If file size >5MB: compress to ≤5MB preserving aspect ratio (bilinear)
   - Log original_size and compressed_size

5. Object Storage write
   - Key pattern: {tenant_id}/{user_id}/{date}/{image_id}.{ext}
   - Encryption: AES-256 SSE
   - Metadata: tenant_id, user_id, session_id, sha256, content_type, original_size

6. Signed URL generation
   - Expiry: 4 hours (aligned with session timeout)
   - Scope: read-only, single resource

7. Audit log write (async, non-blocking)
   - Event: IMAGE_UPLOADED
   - Fields: user_id, tenant_id, image_id, sha256, content_type, size_bytes, session_id, timestamp

8. Response → Client
   - 201 Created with image_id, session_id, metadata
```

### 4.2 Multimodal Query Flow

```
1. Client → API Gateway
   - JWT validation
   - Rate limit check (request-level)
   - Route to Multimodal Query Service

2. Multimodal Query Service
   a. Validate session_id ownership (user must own the session)
   b. Retrieve session context from Context Store
   c. Resolve image_ids → signed URLs from Context Store
   d. Validate all referenced images are available (not expired)

3. Token budget check
   - Calculate estimated tokens: text tokens + image tokens (approx. 765 per image at std resolution)
   - If total session tokens would exceed 8192 (context limit): trigger conversation summarization
   - If after summarization still at risk: return CONTEXT_LIMIT_APPROACHING warning in response

4. LLM Abstraction Layer
   a. Select active vendor (primary: GPT-4o; failover: Claude 3.5 Sonnet)
   b. Construct vendor-specific request:
      - System prompt (use_case-specific from prompt registry)
      - Conversation history (prior turns from session context)
      - Current user query (text + image URLs)
   c. Call vendor API with 30-second timeout
   d. Handle streaming response

5. Response streaming
   - Token-by-token streaming to client via Server-Sent Events (SSE)
   - First token target: ≤2 seconds from query receipt

6. Post-response processing (async)
   a. Append turn to session context store
   b. Update session token_count
   c. Write audit log entry (QUERY_SUBMITTED event)
   d. Increment usage counters for billing/rate limiting

7. Response → Client
   - Stream complete; send done event with usage metadata
```

### 4.3 Session Context Store Data Model

```
Table: vision_sessions
─────────────────────────────────
session_id          STRING PK
tenant_id           STRING
user_id             STRING
created_at          TIMESTAMP
last_activity_at    TIMESTAMP
expires_at          TIMESTAMP
turn_count          INTEGER
token_count         INTEGER
candidate_id        STRING (nullable)
status              ENUM: active | expired | cleared

Table: vision_turns
─────────────────────────────────
turn_id             STRING PK
session_id          STRING FK → vision_sessions
turn_index          INTEGER
role                ENUM: user | assistant
content             TEXT
image_ids           ARRAY<STRING>
created_at          TIMESTAMP
model               STRING (nullable — for assistant turns)
input_tokens        INTEGER (nullable)
output_tokens       INTEGER (nullable)

Table: vision_images
─────────────────────────────────
image_id            STRING PK
tenant_id           STRING
user_id             STRING
session_id          STRING FK → vision_sessions
sha256              STRING
filename            STRING
content_type        STRING
size_bytes          INTEGER
compressed_bytes    INTEGER (nullable)
storage_key         STRING
signed_url          STRING
signed_url_expires  TIMESTAMP
candidate_id        STRING (nullable)
created_at          TIMESTAMP
expires_at          TIMESTAMP (default: created_at + 30 days)
deleted_at          TIMESTAMP (nullable)
```

---

## 5. Model Integration Points

### 5.1 LLM Abstraction Layer Interface

The abstraction layer exposes a single interface to the Multimodal Query Service, regardless of underlying vendor:

```python
class LLMAbstractionLayer:

    async def complete(
        self,
        messages: list[Message],  # includes text + image_url content parts
        system_prompt: str,
        stream: bool = True,
        timeout_seconds: int = 30,
        max_output_tokens: int = 1024,
    ) -> AsyncGenerator[CompletionChunk, None] | CompletionResponse:
        ...

    async def health_check(self) -> VendorHealthStatus:
        ...
```

**Message format (internal):**
```python
@dataclass
class Message:
    role: Literal["user", "assistant"]
    content: list[ContentPart]

@dataclass
class TextContentPart:
    type: Literal["text"] = "text"
    text: str

@dataclass
class ImageContentPart:
    type: Literal["image_url"] = "image_url"
    image_url: ImageURL
    
@dataclass
class ImageURL:
    url: str   # signed S3 URL
    detail: Literal["auto", "low", "high"] = "auto"
```

### 5.2 Vendor-Specific Adapters

**GPT-4o Adapter:**
- Endpoint: `https://api.openai.com/v1/chat/completions`
- Model: `gpt-4o-2025-11` (pinned version — do not use `gpt-4o-latest` in production)
- Image format: URL-based (signed S3 URLs supported natively)
- Token counting: use tiktoken library; images cost 765 tokens at `auto` detail

**Claude 3.5 Sonnet Adapter:**
- Endpoint: `https://api.anthropic.com/v1/messages`
- Model: `claude-3-5-sonnet-20241022`
- Image format: base64 encoded (requires image download from S3 + base64 encoding — adds ~200ms)
- Token counting: Anthropic token counter API; images cost ~1500–4000 tokens depending on size

**Failover Logic:**
```
Primary vendor (GPT-4o) → attempt
  If response received: return
  If timeout (30s) OR status 5xx: 
    log VENDOR_FAILOVER event
    → Secondary vendor (Claude 3.5 Sonnet) → attempt
      If response received: return
      If timeout OR error:
        → Return INFERENCE_UNAVAILABLE error to client
```

### 5.3 System Prompt Registry

System prompts are stored in a versioned registry (not hardcoded) to enable rapid iteration without deployments.

| use_case | System Prompt Key | Description |
|---|---|---|
| `resume_analysis` | `sp_resume_v3` | Optimized for resume extraction and candidate evaluation |
| `whiteboard_analysis` | `sp_whiteboard_v2` | Technical interview artifact interpretation |
| `org_chart_analysis` | `sp_orgchart_v1` | Organizational structure parsing |
| `jd_analysis` | `sp_jd_v2` | Job description extraction and analysis |
| `general` | `sp_general_v4` | Default for unclassified use cases |

All system prompts include:
1. Role context: "You are an AI assistant embedded in HireIQ, an enterprise recruiting platform..."
2. EEO guardrail: "Do not comment on, infer, or make judgments about protected characteristics including race, age, gender, religion, national origin, disability status, or pregnancy. If a resume image contains a candidate photo, do not describe or reference the photo."
3. Output format guidance: specific to use case
4. Uncertainty guidance: "When content in an image is unclear or partially illegible, acknowledge the uncertainty and provide a best-effort interpretation clearly marked as uncertain."

### 5.4 Context Window Management

**Token Budget:**
- Total session token budget: 8,192 tokens (input)
- Approximate image cost: 765 tokens per standard-resolution image (GPT-4o)
- Maximum images without text compression: ~10 images
- In practice with conversation history: ~5 images + 6 turns of conversation

**When budget is approached (>80% utilized):**
1. Warn in response metadata: `"context_warning": "session_approaching_limit"`
2. UI surfaces banner: "This conversation is getting long. Starting a new conversation will give the AI more context to work with."

**When budget is exceeded:**
1. Invoke conversation summarizer: call LLM with current turns and request a 200-token summary
2. Replace oldest 4 conversation turns with summary in context
3. Retain all image references (images are URL-referenced, not embedded in context)
4. Continue conversation with compressed context

---

## 6. Latency Budgets

All targets are measured at p95 unless otherwise noted. These are engineering targets; the SLO for alerting is set at 120% of target.

### 6.1 End-to-End Latency Budget (Image Upload + Query)

| Step | Component | Budget (p95) | Notes |
|---|---|---|---|
| Image upload — client to API gateway | Network | ~200ms | Varies by file size; 1MB image at 10Mbps |
| Image upload — validation + hash | Ingestion Service | 50ms | CPU-bound |
| Image upload — compression (if >5MB) | Ingestion Service | 200ms | Only for large files |
| Image upload — S3 write | Object Storage | 300ms | S3 put latency at p95 |
| Signed URL generation | Ingestion Service | 20ms | |
| **Total image upload** | | **≤800ms** (p95) | |
| | | | |
| Session context retrieval | Context Store | 30ms | Redis-backed |
| Vendor API request construction | Query Service | 10ms | |
| LLM API first token latency | GPT-4o | 1,500ms | Vendor SLA |
| **Time to first token (end-to-end, p95)** | | **≤3,000ms** | Includes upload at 800ms |
| **Time to first token (p50)** | | **≤1,500ms** | Typical case |
| | | | |
| Full response (200 output tokens, p50) | | ≤6,000ms | At ~30 tokens/sec streaming |
| Full response (200 output tokens, p95) | | ≤10,000ms | |

### 6.2 Component-Level Latency SLOs

| Component | Metric | Target | Alert Threshold |
|---|---|---|---|
| Image Ingestion Service | Upload processing time p95 | 800ms | 1,000ms |
| Object Storage (S3) | PUT operation p95 | 300ms | 500ms |
| Context Store (Redis) | GET operation p95 | 10ms | 30ms |
| LLM API (GPT-4o) | Time to first token p95 | 1,500ms | 2,500ms |
| LLM API (GPT-4o) | Availability | 99.9% | <99.5% |
| Multimodal Query Service | Request processing (excl. LLM) p95 | 100ms | 200ms |

### 6.3 Latency Degradation Handling

If LLM API p95 latency exceeds 2,500ms for 5 consecutive minutes:
1. Alert fires to on-call engineer and PM
2. If latency exceeds 4,000ms for 10 consecutive minutes: automatic failover to secondary vendor
3. If secondary vendor also exceeds 4,000ms: return graceful error with retry guidance; text-only queries are unaffected

---

## 7. Storage & Retention

### 7.1 Image Storage

| Storage Layer | Technology | Purpose |
|---|---|---|
| Object storage (primary) | AWS S3 (or S3-compatible) | Persistent image storage |
| CDN / signed URL generation | AWS CloudFront | Serve images to LLM API via signed URL |
| Cache | Redis | Session context, signed URL cache |

**Retention Policy:**

| Customer Configuration | Retention Period | Deletion Method |
|---|---|---|
| Default | 30 days | Automatic S3 lifecycle rule |
| EU customers (GDPR-sensitive) | 7 days (configurable) | Automatic S3 lifecycle rule |
| On explicit deletion request | Immediate | S3 delete + audit log entry |
| On GDPR erasure request | Within 72 hours | Batch deletion job + confirmation |

**Storage Estimations:**

Average image size post-compression: 1.2MB  
Average images per active user per month: 85 (estimated from beta usage data)  
At 500 active users: 500 × 85 × 1.2MB = ~51GB/month new storage  
With 30-day retention: steady-state ~51GB stored  
Cost estimate: $1.17/month at S3 standard pricing — negligible

### 7.2 Session Context Storage

Session context (conversation turns) is stored in Redis with TTL-based expiry:
- Active session TTL: 4 hours from last activity (auto-extended on activity)
- Persistent thread storage: PostgreSQL (vision_turns table) — 30-day retention
- Redis serves as hot cache; PostgreSQL as durable store

---

## 8. Error States & Handling

### 8.1 Error Code Taxonomy

| Error Code | HTTP Status | Description | Client Action |
|---|---|---|---|
| `UNSUPPORTED_FORMAT` | 400 | File format not in whitelist | Show inline error with supported formats |
| `FILE_TOO_LARGE` | 413 | File exceeds 20MB limit | Show size limit error; suggest compression |
| `RATE_LIMIT_EXCEEDED` | 429 | Daily image upload limit reached | Show limit error with reset time |
| `INVALID_SESSION` | 400 | session_id does not exist or expired | Create new session; warn user context was lost |
| `IMAGE_NOT_FOUND` | 404 | Referenced image_id not found or expired | Prompt user to re-upload the image |
| `IMAGE_URL_EXPIRED` | 410 | Signed URL for image has expired | Regenerate URL internally; retry silently |
| `INFERENCE_UNAVAILABLE` | 503 | Both primary and secondary LLM vendor unavailable | Show "AI temporarily unavailable" with retry button |
| `INFERENCE_TIMEOUT` | 504 | LLM API did not respond within 30 seconds | Show timeout error; preserve session; offer retry |
| `CONTEXT_LIMIT_EXCEEDED` | 422 | Session context too large even after summarization | Prompt user to start a new session; link to existing thread |
| `CONTENT_POLICY_VIOLATION` | 422 | Response filtered by content policy | Show generic error; log for ML safety review |
| `ENCRYPTED_PDF` | 400 | PDF is password-protected | Inline error: "Remove password protection and re-upload" |
| `PDF_EXTRACTION_FAILED` | 422 | PDF page extraction failed | Show error with suggestion to upload pages as images |
| `TENANT_QUOTA_EXCEEDED` | 429 | Org-level monthly image quota exceeded | Notify admin; block until quota resets or is raised |
| `FEATURE_NOT_ENABLED` | 403 | User role does not have vision feature access | Explain feature requires admin enablement |

### 8.2 Client-Side Error Rendering Guidelines

All errors are rendered inline in the chat interface — never as modal dialogs that interrupt workflow.

**Error display format:**
```
[Warning icon] [Error message in plain language]
[Optional: specific action link — e.g., "Supported formats ↗"]
```

Errors do not clear the user's text query — the query remains in the input field so the user can modify and resubmit.

### 8.3 Retry Behavior

| Scenario | Automatic Retry | User-Initiated Retry |
|---|---|---|
| `INFERENCE_TIMEOUT` | Once (exponential backoff, 2s delay) | Yes — retry button shown |
| `INFERENCE_UNAVAILABLE` | No (both vendors failed) | Yes — retry button shown |
| `IMAGE_URL_EXPIRED` | Yes, silently (regenerate URL) | N/A |
| Network error (client-side) | Browser-level retry, 1x | Yes — retry button shown |
| `RATE_LIMIT_EXCEEDED` | No | No — show reset time |

### 8.4 Graceful Degradation

If the image processing pipeline is disabled (via feature flag or during incident response):
1. Image attachment controls are hidden from the UI (not just disabled)
2. A banner is shown in the assistant interface: "Image upload is temporarily unavailable. Text queries are working normally."
3. Existing sessions with previously submitted images show images as "expired" with a re-upload prompt
4. No data is lost; text-only assistant functionality is fully unaffected

---

## 9. Security Considerations

### 9.1 Image Data Isolation

- Images are stored with tenant-scoped keys: `{tenant_id}/{user_id}/{date}/{image_id}`
- Signed URLs are user-scoped (IAM policy restricts URL to generating user's tenant)
- No cross-tenant image access is possible via signed URLs — URLs are signed with a tenant-specific IAM role

### 9.2 Signed URL Security

- Expiry: 4 hours (aligned with session timeout)
- URLs are not logged (only the image_id and hash are logged)
- URL rotation: if a signed URL is nearing expiry during an active session, it is silently refreshed before being included in LLM API calls

### 9.3 LLM API Data Handling

- Images are provided to the LLM API via signed URL (GPT-4o) or base64 (Claude)
- LLM vendor DPA explicitly prohibits use of submitted content for model training
- No image content is retained by the LLM vendor beyond the inference request
- All LLM API calls are made from the backend; image URLs are never exposed directly to clients

### 9.4 Input Validation

- MIME type is validated against whitelist (not inferred from file extension)
- Magic bytes check: file header is inspected to confirm MIME type matches declared type
- Maximum file dimensions enforced after decode: images exceeding 4096×4096 are rejected
- SVG files are explicitly blocked (SVG can contain executable content)

### 9.5 Output Filtering

All LLM responses pass through an output filter before delivery to the client:

1. **Content policy filter:** Screens for violent, sexual, or otherwise policy-violating content using a lightweight classifier
2. **PII leakage check:** Detects if the model has echoed back candidate PII in an unexpected format (e.g., outputting a raw SSN from a submitted image) — logs and suppresses if detected
3. **Discrimination risk flag:** Detects mentions of protected characteristics in output and logs for ML safety review

---

## 10. Observability & Monitoring

### 10.1 Key Metrics

**Infrastructure metrics (emitted to Datadog):**

| Metric | Type | Tags |
|---|---|---|
| `vision.image.upload.duration_ms` | Histogram | `tenant_id`, `content_type`, `compressed` |
| `vision.image.upload.success` | Counter | `tenant_id` |
| `vision.image.upload.error` | Counter | `error_code`, `tenant_id` |
| `vision.query.ttft_ms` | Histogram | `vendor`, `use_case`, `image_count` |
| `vision.query.total_duration_ms` | Histogram | `vendor`, `use_case` |
| `vision.query.success` | Counter | `vendor`, `use_case` |
| `vision.query.error` | Counter | `error_code`, `vendor` |
| `vision.vendor.failover` | Counter | `from_vendor`, `to_vendor`, `reason` |
| `vision.context.token_count` | Histogram | `tenant_id` |
| `vision.context.summarization_triggered` | Counter | `tenant_id` |

**Business metrics (emitted to Amplitude):**

| Event | Properties |
|---|---|
| `vision_image_uploaded` | `use_case`, `content_type`, `session_id` |
| `vision_query_submitted` | `image_count`, `use_case`, `query_length` |
| `vision_response_rated` | `rating` (thumbs_up/thumbs_down), `use_case` |
| `vision_context_cleared` | `turn_count`, `image_count` |
| `vision_session_expired` | `session_duration_minutes`, `turn_count` |

### 10.2 Dashboards

**Operational Dashboard (Datadog):**
- Upload success rate (rolling 1h, 24h)
- Query error rate by error_code
- TTFT p50/p95 by vendor
- Vendor failover events
- Active session count

**Product Dashboard (Amplitude):**
- Daily/weekly active vision users (% of eligible)
- Images uploaded per user per day
- Thumbs-up rate by use_case
- Session length distribution

### 10.3 Alerting

| Alert | Condition | Severity | Action |
|---|---|---|---|
| High upload error rate | Error rate >2% over 10 min | P1 | Page on-call engineer |
| TTFT p95 degraded | p95 >3,500ms over 5 min | P2 | Notify on-call; monitor |
| Vendor failover triggered | Any failover event | P2 | Notify on-call; investigate primary |
| Both vendors unavailable | INFERENCE_UNAVAILABLE rate >1% | P0 | Page on-call + PM immediately |
| Storage quota approaching | Tenant at 85% of storage quota | P3 | Notify tenant admin |

---

## 11. Testing Strategy

### 11.1 Unit Tests

- Image validation logic: all supported formats, all rejection cases (oversized, unsupported, password-protected PDF)
- Compression logic: verify output ≤5MB; verify aspect ratio preserved
- SHA-256 deduplication: duplicate detection within session
- Token budget calculation: edge cases at limit
- Error code mapping: all error states return correct HTTP status and body

### 11.2 Integration Tests

- Full upload flow: client → API gateway → ingestion → S3 → signed URL → response
- Full query flow: text + image → query service → LLM abstraction → streaming response → audit log
- Vendor failover: mock GPT-4o timeout; verify Claude adapter receives request
- Session context persistence: multi-turn conversation with image reference in follow-up turn
- Rate limiting: exceed daily limit; verify 429 response and correct reset time

### 11.3 ML/Quality Evaluation

- **Resume extraction benchmark:** 100 resume images across formats (PDF-rendered, photography, LinkedIn export, international formats). Target: ≥90% field accuracy.
- **Whiteboard analysis benchmark:** 30 whiteboard images across technical topics. Human raters score output "useful / partially useful / not useful." Target: ≥70% "useful."
- **Org chart parsing benchmark:** 20 org chart images of varying complexity. Target: ≥80% correct node identification.
- **EEO guardrail evaluation:** 20 test prompts designed to elicit protected characteristic commentary. Zero violations required to pass.
- **Adversarial inputs:** 10 images designed to test edge cases (blank, logo, rotated, low-resolution, multi-language). Verify graceful handling per EC-001 through EC-006.

### 11.4 Load Testing

- Scenario: 500 concurrent users each submitting 1 image upload + 2 queries in a 5-minute window
- Target: upload p95 ≤1,000ms; TTFT p95 ≤3,500ms; error rate <0.5%
- Tool: k6 (configured load test scripts in `/tests/load/`)
- Required: pass load test before beta launch and before GA

### 11.5 Security Testing

- Penetration test: image upload endpoint (included in scope of Q2 2026 pen test engagement)
- Signed URL isolation: verify cross-tenant URL usage is rejected
- Magic bytes validation: attempt to upload executable disguised as image — must be rejected
- Content injection: attempt prompt injection via image text content — verify system prompt is not overridden
