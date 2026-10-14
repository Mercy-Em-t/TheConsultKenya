# Sequence Diagram: SQ_UC15 — Review and Approve Escrow Milestone
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC15`  
**Author:** Principal Object Solutions Architect  
**Date:** October 2026  

---

## 1. Interaction Overview & Lifelines
- **Primary Actor:** Initiating user or scheduled daemon trigger.
- **Boundary / UI:** Web interface or modal dialogue receiving keystrokes and rendering feedback.
- **Control / Domain Services:** Orchestrates business invariants and invokes algorithms.
- **Entity / Persistence:** Persistent relational data stores, Redis caches, and S3 vaults.
- **External Gateways:** Third-party integrations (Safaricom Daraja, KRA eTIMS, LiveKit SFU).

---

## 2. UML Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Client as 👤 Client
    participant UI as 🖥️ MilestoneApprovalUI
    participant EscrowFSM as ⚙️ EscrowStateMachine (PROG-06)
    participant TaxEngine as ⚙️ KRAeTIMSPayoutEngine (PROG-07)
    participant KRA as 🏛️ KRA eTIMS OSCU
    participant Daraja as 🏛️ Safaricom Daraja B2C
    participant Ledger as 🗄️ DoubleEntryLedgerService

    Client->>UI: Clicks "Approve Deliverable & Release Funds"
    activate UI
    UI->>EscrowFSM: approveMilestone(milestoneId, clientId)
    activate EscrowFSM
    EscrowFSM->>EscrowFSM: transitionTo("APPROVED_RELEASED")
    
    %% Tax & Payout Execution
    EscrowFSM->>TaxEngine: executeDisbursementAndTaxInvoicing(milestoneId, gross=50000)
    activate TaxEngine
    TaxEngine->>TaxEngine: calculateSplit(gross=50000, fee=3500 [7%], wht=2500 [5%], net=44000)
    
    TaxEngine->>KRA: signFiscalInvoice(gross=50000, fee=3500, vat=560)
    activate KRA
    KRA-->>TaxEngine: {controlCode: "SCU01928374", qrPayload: "https://etims.kra.go.ke/..."}
    deactivate KRA

    TaxEngine->>Ledger: postThreeLegSettlement(PLATFORM_REVENUE=3500, KRA_WHT=2500, CONSULTANT=44000)
    TaxEngine->>Daraja: POST /mpesa/b2c/v1/paymentrequest (amount=44000, phone=consultantPhone)
    activate Daraja
    Daraja-->>TaxEngine: B2C ConversationID Dispatched
    deactivate Daraja
    TaxEngine-->>EscrowFSM: SettlementCompleteReceipt()
    deactivate TaxEngine

    EscrowFSM-->>UI: ReleaseSuccess()
    deactivate EscrowFSM
    UI-->>Client: Displays Formal eTIMS Tax Invoice with QR Code
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
