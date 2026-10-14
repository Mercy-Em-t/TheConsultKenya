# Specification-Level Domain Model
*System: Consult Kenya (Visual-First Professional Advisory & Authority Network)*
*Grounded in RAG Knowledge Cards `CARD-001` through `CARD-010` and Jackson-Zave Problem Frames*

---

## 1. Philosophical & Ontological Framework
According to modern Requirements Engineering principles (Jackson & Zave), software does not operate in a vacuum. It interacts with the physical world at a shared interface:
$$\text{Environment } (E) \land \text{Specification } (S) \implies \text{Requirement } (R)$$

To make requirements verifiable and prevent ungrounded assumptions, we categorize all system elements into three distinct classes of phenomena:

```mermaid
flowchart TD
    subgraph EP["1. Environmental Phenomena (Real-World / Uncontrolled by Machine)"]
        E1["Human professional competence & experience"]
        E2["Safaricom mobile network connectivity & tower signal"]
        E3["Physical client inspection of delivered code / architecture"]
        E4["Statutory legality of advisory contracts under Kenyan Law"]
        E5["Human willingness to pay & enter mobile M-Pesa PIN"]
    end

    subgraph SP["2. Shared Phenomena (Boundary Interface / Monitored & Controlled)"]
        S1["Touch gestures, carousel swipes, UI button clicks"]
        S2["M-Pesa STK push payloads & gateway webhook callbacks"]
        S3["Uploaded deliverable asset files (PDFs, ZIPs, code repos)"]
        S4["Calendar slot selection & mutual WebRTC session joins"]
        S5["Digital signature hashes & intake question responses"]
    end

    subgraph MP["3. Machine Phenomena (Internal Software State / Strictly Controlled)"]
        M1["Creator Authority Score (CAS) formula evaluation"]
        M2["128-dimensional dense vector embeddings in database"]
        M3["Escrow ledger double-entry debit/credit journals"]
        M4["Two-pass ranking algorithm candidate score calculation"]
        M5["Row-Level Security (RLS) policy enforcement logic"]
        M6["72-hour and 7-day automated inspection countdown timers"]
    end

    EP <-->|Physical Reality Grounding| SP
    SP <-->|API / Hardware Sensors & Screens| MP
```

---

## 2. Comprehensive Domain Entity Architecture

The entity-relationship diagram below models the core domain entities, their state attributes, and their relationships across the 22 core use cases.

```mermaid
erDiagram
    USER ||--o{ CONSULTANT_PROFILE : "specializes as"
    USER ||--o{ BOOKMARK : "saves"
    USER ||--o{ BOOKING : "schedules as client"
    
    CONSULTANT_PROFILE ||--o{ CASE_STUDY : "authors"
    CONSULTANT_PROFILE ||--o{ CREDENTIAL_RECORD : "verifies"
    CONSULTANT_PROFILE ||--o{ CALENDAR_CONFIG : "configures"
    CONSULTANT_PROFILE ||--o{ BOOKING : "hosts as consultant"
    CONSULTANT_PROFILE ||--o{ ESCROW_CONTRACT : "executes work"
    
    CASE_STUDY ||--o{ CASE_SLIDE : "contains"
    CASE_STUDY ||--o{ EVIDENCE_PROOF : "attaches"
    CASE_STUDY ||--o{ CONVERSION_ANCHOR : "embeds"
    CASE_STUDY ||--o{ BOOKMARK : "saved by"
    CASE_STUDY ||--o{ TELEMETRY_EVENT : "generates"
    
    BOOKING ||--|| PAYMENT_TRANSACTION : "funded by"
    BOOKING ||--o| LIVE_ROOM_SESSION : "launches"
    
    ESCROW_CONTRACT ||--o{ MILESTONE : "structured into"
    MILESTONE ||--o| PAYMENT_TRANSACTION : "funded by"
    MILESTONE ||--o{ DELIVERABLE_ASSET : "contains"
    MILESTONE ||--o| DISPUTE_CASE : "escalated to"
    
    PAYMENT_TRANSACTION ||--o| ETIMS_TAX_INVOICE : "generates"
    
    USER {
        uuid user_id PK
        string national_id
        string phone_number
        string email
        string full_name
        string kra_pin
        enum user_role
        timestamp created_at
    }

    CONSULTANT_PROFILE {
        uuid profile_id PK
        uuid user_id FK
        string professional_title
        string primary_discipline
        enum verification_tier
        decimal creator_authority_score
        decimal hourly_rate_kes
        boolean is_founding_creator
    }

    CASE_STUDY {
        uuid post_id PK
        uuid consultant_id FK
        string title
        enum template_type
        enum content_format
        string category_tag
        boolean is_quarantined
        timestamp published_at
    }

    CASE_SLIDE {
        uuid slide_id PK
        uuid post_id FK
        int slide_index
        string slide_heading
        text slide_body_text
        string code_snippet
        string diagram_mermaid
    }

    EVIDENCE_PROOF {
        uuid proof_id PK
        uuid post_id FK
        string github_repo_url
        string commit_sha
        uuid client_coauthor_id FK
        boolean is_redacted
    }

    CONVERSION_ANCHOR {
        uuid anchor_id PK
        uuid post_id FK
        enum anchor_type
        decimal price_kes
        string custom_cta_label
    }

    BOOKING {
        uuid booking_id PK
        uuid client_id FK
        uuid consultant_id FK
        timestamp start_time
        timestamp end_time
        enum booking_status
        json intake_answers
    }

    ESCROW_CONTRACT {
        uuid contract_id PK
        uuid client_id FK
        uuid consultant_id FK
        string project_title
        decimal total_value_kes
        enum contract_status
        string statement_of_work_hash
    }

    MILESTONE {
        uuid milestone_id PK
        uuid contract_id FK
        int milestone_sequence
        string milestone_title
        decimal milestone_amount_kes
        enum milestone_status
        timestamp due_date
        timestamp auto_approval_deadline
    }

    DELIVERABLE_ASSET {
        uuid asset_id PK
        uuid milestone_id FK
        string file_name
        string sha256_checksum
        string storage_uri
        timestamp uploaded_at
    }

    DISPUTE_CASE {
        uuid dispute_id PK
        uuid milestone_id FK
        uuid initiator_id FK
        text dispute_grounds
        enum dispute_status
        decimal arbitrated_refund_ratio
        timestamp filed_at
    }

    PAYMENT_TRANSACTION {
        uuid transaction_id PK
        string mpesa_receipt_number
        decimal gross_amount_kes
        decimal platform_take_fee_kes
        decimal net_payout_kes
        enum payment_rail
        enum payment_status
    }

    ETIMS_TAX_INVOICE {
        uuid invoice_id PK
        uuid transaction_id FK
        string fiscal_signature
        string kra_qr_code_url
        timestamp generated_at
    }
```

---

## 3. Entity Classification & Lifecycle States

### 1. `CONSULTANT_PROFILE` Lifecycle
* `PENDING_KYC` $\to$ `BRONZE_VERIFIED` (ID/KRA valid) $\to$ `SILVER_VERIFIED` (Statutory Board valid) $\to$ `GOLD_MASTER` ($\ge 10$ Escrow completions & CAS $\ge 8.5$).
* Invalidation: Any annual board failure triggers `PROVISIONAL_HOLD`.

### 2. `MILESTONE` Lifecycle
* `DRAFT` $\to$ `PENDING_FUNDING` $\to$ `FUNDED_IN_PROGRESS` $\to$ `SUBMITTED_IN_REVIEW` $\to$ `APPROVED_RELEASED` (or `AUTO_APPROVED`).
* Exception Paths:
  * `REVISION_REQUESTED` (loops back to `FUNDED_IN_PROGRESS`).
  * `DISPUTED` (freezes countdown, moves to `DISPUTE_CASE`).

### 3. `DISPUTE_CASE` Lifecycle
* `OPEN_EVIDENCE_PERIOD` (48h mutual submission) $\to$ `AMICABLE_NEGOTIATION` (prorated split signed) OR `MEDIATOR_REVIEW` $\to$ `BINDING_RULING_EXECUTED` (or `ESCALATED_CIARB_ARBITRATION`).
