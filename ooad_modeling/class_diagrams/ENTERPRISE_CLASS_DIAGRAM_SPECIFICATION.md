# ENTERPRISE DOMAIN CLASS DIAGRAM SPECIFICATION
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 (Class Modeling)  
**Lifecycle Stage:** Object-Oriented Analysis & Design  
**Author:** Principal Object Solutions Architect  
**Date:** October 2026  

---

## 1. Domain Class Architecture & Design Principles

The Consult Kenya domain model is architected following **Domain-Driven Design (DDD)** and Object-Oriented principles:
- **Entity Abstractions:** Domain classes with distinct identity (`User`, `ConsultantProfile`, `CaseStudyDeck`, `BookingSlot`, `EscrowContract`, `EscrowMilestone`, `DisputeCase`, `LedgerTransaction`).
- **Encapsulated Invariants:** Methods enforce valid business logic transitions. Attribute mutations are strictly private (`-`) and accessed through public (`+`) typed operations.
- **Inheritance Hierarchies:** A generalized `User` base class specialized into `Consultant`, `Client`, and `Mediator`.
- **Composition & Aggregation:** An `EscrowContract` **composes** multiple `EscrowMilestone` instances (milestones cannot exist without a contract). A `CaseStudyDeck` **aggregates** `EvidenceProof` items.

---

## 2. High-Level UML Class Diagram

```mermaid
classDiagram
    direction TB

    %% Inheritance Hierarchy
    class User {
        -UUID id
        -String fullName
        -String email
        -String phoneE164
        -String passwordHash
        -UserRole role
        -AccountStatus accountStatus
        -DateTime createdAt
        +verifyPassword(rawPassword: String) Boolean
        +generateAuthTokenPair() TokenPair
        +updateProfile(fullName: String, phone: String) Void
    }

    class Consultant {
        -AuthorityTier authorityTier
        -String professionalBio
        -Decimal hourlyRateKes
        -Float casScore
        -String kraPin
        -List~String~ practiceAreas
        -JSONB bentoGridLayout
        +submitCredentials(licenseNo: String, board: CredentialType) CredentialVerification
        +publishCaseStudy(draft: CaseStudyDraft) CaseStudyDeck
        +setAvailabilitySchedule(slots: List~TimeRange~) Void
        +withdrawEarnings(amount: Decimal) PayoutReceipt
    }

    class Client {
        -String companyName
        -String companyKRAPin
        -String industrySector
        -Decimal accountBalanceKes
        +lockConsultationSlot(consultantId: UUID, slotTime: DateTime) SlotLockToken
        +fundMilestoneEscrow(milestoneId: UUID, paymentMethod: PaymentMethod) Boolean
        +approveMilestoneDeliverable(milestoneId: UUID) ApprovalReceipt
        +lodgeDispute(milestoneId: UUID, reason: String, evidence: List~Doc~) DisputeCase
    }

    class Mediator {
        -String ciarbAccreditationNo
        -Int activeCaseCount
        -Boolean isAvailable
        +reviewDossier(caseId: UUID) DisputeDossier
        +conductHearing(caseId: UUID, sessionNotes: String) Void
        +issueBindingRuling(caseId: UUID, clientPct: Decimal, consultantPct: Decimal) AdjudicationAward
    }

    User <|-- Consultant : Generalization
    User <|-- Client : Generalization
    User <|-- Mediator : Generalization

    %% Authority & Content Domain
    class CaseStudyDeck {
        -UUID id
        -UUID authorId
        -String title
        -String slug
        -String markdownContent
        -String sanitizedHtml
        -PublicationStatus status
        -List~Float~ semanticEmbedding256D
        -DateTime publishedAt
        +compileMarkdown() CompiledView
        +renderMermaidSVGs() List~SVGNode~
        +generateVectorEmbedding() List~Float~
        +attachConversionAnchor(ctaType: String, targetSlotId: UUID) Void
    }

    class EvidenceProof {
        -UUID id
        -ProofType proofType
        -String title
        -String artifactUrl
        -String sha256Fingerprint
        -DateTime verifiedAt
        +validateIntegrity(fileBytes: ByteStream) Boolean
    }

    Consultant "1" --> "*" CaseStudyDeck : Authors
    CaseStudyDeck "1" *-- "*" EvidenceProof : Composes

    %% Booking & Calendar Domain
    class BookingSlot {
        -UUID id
        -UUID consultantId
        -UUID clientId
        -DateTime scheduledStartTime
        -DateTime scheduledEndTime
        -BookingStatus status
        -String distributedLockToken
        -DateTime lockExpiresAt
        +acquireSoftLock(clientId: UUID, ttlSeconds: Int) Boolean
        +confirmBooking(mpesaReceipt: String) Void
        +cancelReservation(reason: String) Void
    }

    Consultant "1" --> "*" BookingSlot : Schedules
    Client "1" --> "*" BookingSlot : Books

    %% Escrow & Milestone Domain
    class EscrowContract {
        -UUID id
        -UUID clientId
        -UUID consultantId
        -String projectTitle
        -Decimal totalBudgetKes
        -Decimal heldTrustBalanceKes
        -ContractStatus contractStatus
        -DateTime createdAt
        +createMilestone(title: String, amount: Decimal) EscrowMilestone
        +depositFunds(amount: Decimal, transactionRef: String) Void
        +closeContract() Void
    }

    class EscrowMilestone {
        -UUID id
        -UUID contractId
        -String title
        -Decimal milestoneBudgetKes
        -MilestoneStatus milestoneStatus
        -String deliverableUri
        -String deliverableSha256
        -DateTime submittedAt
        -DateTime autoApprovalDeadline
        +fundMilestone(depositRef: String) Void
        +submitDeliverable(fileUri: String, checksum: String) Void
        +approveAndRelease() SettlementReceipt
        +freezeForDispute() Void
    }

    EscrowContract "1" *-- "1..*" EscrowMilestone : Composes
    Client "1" --> "*" EscrowContract : Commissions
    Consultant "1" --> "*" EscrowContract : Performs

    %% Dispute Domain
    class DisputeCase {
        -UUID caseId
        -UUID milestoneId
        -UUID claimantId
        -UUID mediatorId
        -DisputeReason reasonCategory
        -DisputeStatus caseStatus
        -Decimal splitClientPct
        -Decimal splitConsultantPct
        -String certificateUrl
        -DateTime rebuttalDeadline
        +submitCounterEvidence(respondentId: UUID, docUri: String) Void
        +assignMediator(mediatorId: UUID) Void
        +executeDisbursement() Void
    }

    EscrowMilestone "1" --> "0..1" DisputeCase : Subject to
    Mediator "1" --> "*" DisputeCase : Adjudicates

    %% Financial Ledger & Settlement Domain
    class LedgerTransaction {
        -UUID transactionId
        -String debitAccount
        -String creditAccount
        -Decimal amountKes
        -String externalReference
        -PaymentRail railType
        -DateTime createdAt
        +postDoubleEntry() Boolean
        +reconcileStatement(bankStatementRef: String) Boolean
    }

    class TaxInvoice {
        -UUID invoiceId
        -UUID milestoneId
        -String invoiceNumber
        -String kraControlCode
        -String qrCodePayload
        -Decimal grossAmountKes
        -Decimal platformFeeKes
        -Decimal vatAmountKes
        -Decimal whtDeductionKes
        -Decimal netPayoutKes
        -DateTime issuedAt
        +signWithKRAeTIMS() Boolean
        +verifyQRData() String
    }

    EscrowMilestone "1" --> "1" TaxInvoice : Generates
    TaxInvoice "1" --> "1..*" LedgerTransaction : Reconciles
```

---

## 3. Class Specifications (Attributes & Operations Detail)

### 3.1 Class `User` (Abstract Domain Model)
- **Attributes:**
  - `- id: UUID`: Unique uniform identifier (UUIDv7 timestamp-ordered).
  - `- fullName: String`: Legal name verified against government records.
  - `- email: String`: Primary contact and notification address.
  - `- phoneE164: String`: Kenyan mobile subscriber number (`+2547XXXXXXXX`).
  - `- passwordHash: String`: Salted Argon2id / PBKDF2 cryptographic digest.
  - `- role: UserRole`: Enumerated privilege (`CLIENT`, `CONSULTANT`, `MEDIATOR`, `ADMIN`).
  - `- accountStatus: AccountStatus`: Active, suspended, or pending verification.
- **Operations:**
  - `+ verifyPassword(rawPassword: String): Boolean`: Constant-time hash comparison.
  - `+ generateAuthTokenPair(): TokenPair`: Issues HMAC-SHA256 JWT access and refresh tokens.

### 3.2 Class `Consultant` (Specialization of `User`)
- **Attributes:**
  - `- authorityTier: AuthorityTier`: `TIER_1_EMERGING`, `TIER_2_ESTABLISHED`, `TIER_3_AUTHORITY`.
  - `- hourlyRateKes: Decimal`: Hourly consultation tariff in Kenya Shillings.
  - `- casScore: Float`: Dynamic Creator Authority Score (0.0 to 1000.0).
  - `- kraPin: String`: Verified 11-character taxpayer PIN (`A012345678W`).
  - `- bentoGridLayout: JSONB`: Visual portfolio cards and evidence widgets.
- **Operations:**
  - `+ submitCredentials(licenseNo: String, board: CredentialType): CredentialVerification`: Queries statutory registry APIs (LSK, ICPAK, EBK) and auto-upgrades authority tier upon verification.
  - `+ publishCaseStudy(draft: CaseStudyDraft): CaseStudyDeck`: Triggers Markdown parsing, Mermaid SVG compilation, and 256-dim embedding generation.

### 3.3 Class `EscrowMilestone` (Component of `EscrowContract`)
- **Attributes:**
  - `- id: UUID`: Primary milestone identifier.
  - `- milestoneBudgetKes: Decimal`: Cent-precise milestone financial allocation.
  - `- milestoneStatus: MilestoneStatus`: `PENDING_FUNDING`, `FUNDED_LOCKED`, `SUBMITTED`, `APPROVED_RELEASED`, `REVISIONS_REQUESTED`, `FROZEN_DISPUTE`.
  - `- deliverableSha256: String`: Cryptographic checksum of delivered work.
  - `- autoApprovalDeadline: DateTime`: Timestamp 72 hours post-submission.
- **Operations:**
  - `+ fundMilestone(depositRef: String): Void`: Transitions state to `FUNDED_LOCKED` upon verified M-Pesa receipt.
  - `+ submitDeliverable(fileUri: String, checksum: String): Void`: Locks deliverable payload, starts 72-hour auto-approval clock.
  - `+ approveAndRelease(): SettlementReceipt`: Computes 7% platform fee, 5% WHT, 16% VAT, executes ledger entries, and triggers Safaricom B2C payout.

### 3.4 Class `TaxInvoice` (KRA Fiscal Entity)
- **Attributes:**
  - `- invoiceNumber: String`: Sequential unique electronic tax invoice ID.
  - `- kraControlCode: String`: Cryptographic fiscal signature from KRA OSCU.
  - `- qrCodePayload: String`: Official KRA URL verification string.
  - `- platformFeeKes: Decimal`: 7% gross commission.
  - `- vatAmountKes: Decimal`: 16% VAT assessed on platform fee.
  - `- whtDeductionKes: Decimal`: 5% statutory professional Withholding Tax.
  - `- netPayoutKes: Decimal`: Net disbursed consultant balance.
- **Operations:**
  - `+ signWithKRAeTIMS(): Boolean`: Communicates with eTIMS fiscal control unit.
  - `+ verifyQRData(): String`: Returns scannable public tax validation link.
