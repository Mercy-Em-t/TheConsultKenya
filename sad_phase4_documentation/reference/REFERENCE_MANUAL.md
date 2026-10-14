# CONSULT KENYA: TECHNICAL REFERENCE MANUAL
**Document Type:** Formal System Reference Document  
**Audience:** Software Engineers, DevOps Engineers, Security Auditors, Database Administrators  
**Lifecycle Stage:** Phase 4 — Implementation & Production Reference  
**Version:** 1.0 (Production Master)  

---

## 1. Table of Contents & Navigation Index

- [1. Table of Contents & Navigation Index](#1-table-of-contents--navigation-index)
- [2. System Architecture & Topology Reference](#2-system-architecture--topology-reference)
  - [2.1 [Inspect Topology] Physical Deployment Specifications](#21-inspect-topology-physical-deployment-specifications)
  - [2.2 [Configure Environment] Variable & Secret Reference](#22-configure-environment-variable--secret-reference)
- [3. Core Module & API Specifications Reference](#3-core-module--api-specifications-reference)
  - [3.1 [Authenticate Identity] PROG-01 Verification API](#31-authenticate-identity-prog-01-verification-api)
  - [3.2 [Query Vectors] PROG-03 Vector Search API](#32-query-vectors-prog-03-vector-search-api)
  - [3.3 [Acquire Lock] PROG-04 Distributed Slot Lock API](#33-acquire-lock-prog-04-distributed-slot-lock-api)
  - [3.4 [Initiate Payment] PROG-05 M-Pesa Daraja STK Push API](#34-initiate-payment-prog-05-m-pesa-daraja-stk-push-api)
  - [3.5 [Transition State] PROG-06 Escrow State Machine API](#35-transition-state-prog-06-escrow-state-machine-api)
  - [3.6 [Generate Invoice] PROG-07 KRA eTIMS & Payout API](#36-generate-invoice-prog-07-kra-etims--payout-api)
  - [3.7 [Arbitrate Case] PROG-08 Dispute Adjudication API](#37-arbitrate-case-prog-08-dispute-adjudication-api)
- [4. Data Dictionary & Physical Schema Reference](#4-data-dictionary--physical-schema-reference)
- [5. Error Code & Exception Dictionary](#5-error-code--exception-dictionary)
- [6. Two-Part Navigation Index & Keyword Directory](#6-two-part-navigation-index--keyword-directory)

---

## 2. System Architecture & Topology Reference

### 2.1 [Inspect Topology] Physical Deployment Specifications
Consult Kenya is deployed on AWS Cape Town (`af-south-1`) with Cloudflare Edge Anycast:
- **Application Servers:** 4x ECS Fargate instances (2 vCPU, 4GB RAM each). Auto-scaling threshold: 70% CPU / 1000 concurrent connections.
- **Relational Data Store:** AWS RDS PostgreSQL 16.2 Multi-AZ with `pgvector` extension.
- **Cache & Lock Store:** AWS ElastiCache Redis 7.2 (Cluster mode enabled).
- **Blob Storage:** AWS S3 with KMS CMK encryption (`arn:aws:kms:af-south-1:...`) and immutable lifecycle policies.
- **WebRTC SFU:** LiveKit Cloud Enterprise (Media relay via Liquid Telecom & Safaricom interconnects).

### 2.2 [Configure Environment] Variable & Secret Reference
All configuration variables are managed via AWS Secrets Manager and loaded at startup:
- `DATABASE_URL`: Connection string (`postgresql+asyncpg://user:pass@host:5432/consultkenya`).
- `REDIS_URL`: Connection string (`rediss://default:pass@redis-cluster:6379/0`).
- `JWT_SECRET_KEY`: 512-bit cryptographically random HMAC secret for session authentication.
- `DARAJA_CONSUMER_KEY` & `DARAJA_CONSUMER_SECRET`: Safaricom Daraja APIv2 credentials.
- `DARAJA_PASSKEY`: Safaricom STK Push passkey string.
- `KRA_ETIMS_OSCU_KEY`: Hardware/software security module API token for fiscal signing.
- `LIVEKIT_API_KEY` & `LIVEKIT_API_SECRET`: Video room generation keys.

---

## 3. Core Module & API Specifications Reference

### 3.1 [Authenticate Identity] PROG-01 Verification API
- **Endpoint:** `POST /api/v1/auth/register`
- **Request Headers:** `Content-Type: application/json`
- **Payload Schema:**
  ```json
  {
    "full_name": "Dr. Beatrice Muthoni",
    "phone": "+254712345678",
    "national_id": "24987654",
    "password": "SecurePassword2026!",
    "role": "CONSULTANT"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "user_id": "018f3a9e-4c7b-7221-a120-cf91b8f10283",
    "token": "eyJhbGciOiJIUzI1Ni...",
    "token_type": "Bearer",
    "kyc_status": "PENDING_IPRS"
  }
  ```

### 3.2 [Query Vectors] PROG-03 Vector Search API
- **Endpoint:** `POST /api/v1/search/vector`
- **Payload Schema:**
  ```json
  {
    "query": "Land dispute title deed verification Machakos County",
    "top_k": 5,
    "category": "CONVEYANCING_LAW"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "matches": [
      {
        "consultant_id": "c-901",
        "name": "Adv. James Mutiso",
        "similarity_score": 0.912,
        "hourly_rate_kes": 7500.00,
        "video_brief_url": "https://cdn.consultkenya.co.ke/briefs/c901.mp4"
      }
    ]
  }
  ```

### 3.3 [Acquire Lock] PROG-04 Distributed Slot Lock API
- **Endpoint:** `POST /api/v1/slots/lock`
- **Payload Schema:**
  ```json
  {
    "consultant_id": "c-901",
    "start_time": "2026-11-10T10:00:00+03:00",
    "end_time": "2026-11-10T11:00:00+03:00"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "lock_token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "ttl_seconds": 900,
    "status": "RESERVED"
  }
  ```

### 3.4 [Initiate Payment] PROG-05 M-Pesa Daraja STK Push API
- **Endpoint:** `POST /api/v1/payments/stkpush`
- **Payload Schema:**
  ```json
  {
    "booking_id": "BKG-9921",
    "phone": "+254712345678",
    "amount_kes": 7500.00
  }
  ```
- **Response (202 Accepted):**
  ```json
  {
    "checkout_request_id": "ws_CO_1210202620450091823",
    "merchant_request_id": "9812-441-1",
    "response_code": "0",
    "status": "PENDING_USER_PIN"
  }
  ```

### 3.5 [Transition State] PROG-06 Escrow State Machine API
- **Endpoint:** `POST /api/v1/escrow/transition`
- **Payload Schema:**
  ```json
  {
    "milestone_id": "M-881",
    "action": "APPROVE_DELIVERABLE",
    "client_id": "u-401"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "milestone_id": "M-881",
    "previous_state": "SUBMITTED",
    "current_state": "APPROVED_RELEASED",
    "payout_triggered": true
  }
  ```

### 3.6 [Generate Invoice] PROG-07 KRA eTIMS & Payout API
- **Endpoint:** `POST /api/v1/payouts/process`
- **Calculation Formula:**
  - $\text{Gross Amount} = K$
  - $\text{Withholding Tax (WHT 5\%)} = 0.05 \times K$
  - $\text{Platform Commission (7\%)} = 0.07 \times K$
  - $\text{VAT on Commission (16\%)} = 0.16 \times (0.07 \times K)$ (borne by the platform, inside the commission)
  - $\text{Net Consultant Payout} = K - \text{WHT} - \text{Platform Commission}$
- **Response (200 OK):** Fiscal invoice receipt with KRA control code and Safaricom B2C conversation token.

### 3.7 [Arbitrate Case] PROG-08 Dispute Adjudication API
- **Endpoint:** `POST /api/v1/disputes/rule`
- **Payload Schema:**
  ```json
  {
    "dispute_id": "DSP-109",
    "client_split_pct": 50.00,
    "consultant_split_pct": 50.00,
    "arbitrator_notes": "Deliverable partially completed; 50% split awarded."
  }
  ```
- **Response (200 OK):** Case resolved; split refund queued for instant disbursement.

---

## 4. Data Dictionary & Physical Schema Reference

| Table Name | Primary Key | Key Attributes | Constraints & Indexes |
| :--- | :--- | :--- | :--- |
| `users` | `id` (UUIDv7) | `phone_e164`, `password_hash`, `role`, `kyc_status` | `UNIQUE(phone_e164)` |
| `consultant_profiles` | `id` (UUIDv7) | `user_id`, `specialty`, `hourly_rate`, `kra_pin`, `authority_score` | `FK(users.id)`, `INDEX(specialty)` |
| `media_transcripts` | `id` (UUIDv7) | `consultant_id`, `chunk_text`, `embedding` (vector(256)) | `HNSW (embedding vector_cosine_ops)` |
| `booking_slots` | `id` (UUIDv7) | `consultant_id`, `client_id`, `start_time`, `end_time`, `status` | `UNIQUE(consultant_id, start_time)` |
| `escrow_accounts` | `id` (UUIDv7) | `contract_id`, `total_amount`, `held_amount`, `released_amount` | `CHECK(held_amount >= 0)` |
| `milestones` | `id` (UUIDv7) | `escrow_id`, `title`, `amount`, `status`, `delivered_at` | `INDEX(status)` |
| `tax_invoices` | `id` (UUIDv7) | `milestone_id`, `invoice_no`, `kra_control_code`, `qr_data` | `UNIQUE(invoice_no)` |
| `disputes` | `id` (UUIDv7) | `milestone_id`, `claimant_id`, `arbitrator_id`, `split_client` | `FK(milestones.id)` |

---

## 5. Error Code & Exception Dictionary

| HTTP Code | Error Slug / Code | Underlying Exception | Cause & Recommended System Remediation |
| :---: | :--- | :--- | :--- |
| **400** | `INVALID_MEDIA_CONTAINER` | `InvalidMediaContainerError` | Uploaded video has non-standard codecs. Re-encode to H.264/AAC. |
| **403** | `FORBIDDEN_ROLE_ACTION` | `InsufficientPrivilegesError` | Caller role lacks required privilege. Check RBAC claims in JWT. |
| **409** | `SLOT_ALREADY_RESERVED` | `SlotContentionConflictError` | Slot was locked by another user. Refresh slot availability grid. |
| **410** | `LOCK_TTL_EXPIRED` | `LockTTLExpiredError` | User took longer than 900s to complete checkout. Must re-reserve slot. |
| **422** | `INVALID_KENYAN_PHONE` | `ValidationError` | Mobile number violates E.164 (`+254...`). Rectify phone input string. |
| **422** | `INVALID_KRA_PIN` | `ValidationError` | KRA PIN format does not match 11-char pattern. Verify taxpayer certificate. |
| **502** | `DARAJA_GATEWAY_ERROR` | `DarajaGatewayTimeoutError` | Safaricom API returned timeout or 503. Retry transaction via queue. |
| **503** | `ETIMS_OSCU_UNAVAILABLE` | `ETIMSOfflineError` | KRA signing device offline. Invoice marked pending sync; retry in background. |

---

## 6. Two-Part Navigation Index & Keyword Directory

Use this index to quickly locate system operations by **Action + Subject**:

| Two-Part Term (Action + Subject) | Reference Link | Primary System Context |
| :--- | :--- | :--- |
| **[Acquire Lock]** | [Section 3.3](#33-acquire-lock-prog-04-distributed-slot-lock-api) | Distributed calendar slot reservation & Redis TTL |
| **[Arbitrate Case]** | [Section 3.7](#37-arbitrate-case-prog-08-dispute-adjudication-api) | Dispute resolution, dossier review & split awards |
| **[Authenticate Identity]** | [Section 3.1](#31-authenticate-identity-prog-01-verification-api) | User registration, password salting, JWT issuance |
| **[Configure Environment]**| [Section 2.2](#22-configure-environment-variable--secret-reference) | Environment keys, secrets, database connection strings |
| **[Generate Invoice]** | [Section 3.6](#36-generate-invoice-prog-07-kra-etims--payout-api) | KRA eTIMS fiscalization & withholding tax arithmetic |
| **[Initiate Payment]** | [Section 3.4](#34-initiate-payment-prog-05-m-pesa-daraja-stk-push-api) | Safaricom Daraja STK Push trigger & callback handling |
| **[Inspect Topology]** | [Section 2.1](#21-inspect-topology-physical-deployment-specifications) | Physical hardware, cloud instances & network links |
| **[Query Vectors]** | [Section 3.2](#32-query-vectors-prog-03-vector-search-api) | Two-pass pgvector cosine search & reranking |
| **[Resolve Error]** | [Section 5](#5-error-code--exception-dictionary) | Troubleshooting HTTP status codes & exception catalog |
| **[Transition State]** | [Section 3.5](#35-transition-state-prog-06-escrow-state-machine-api) | Milestone escrow FSM state progressions |
