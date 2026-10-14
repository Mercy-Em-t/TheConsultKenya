# Sequence Diagram: SQ_UC13 — Fund Milestone Escrow Contract
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC13`  
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
    participant UI as 🖥️ EscrowContractUI
    participant EscrowFSM as ⚙️ EscrowStateMachine (PROG-06)
    participant Daraja as 🏛️ Safaricom Daraja API
    participant DB as 🗄️ tbl_escrow_milestones

    Client->>UI: Selects Milestone 1 (KES 50,000) & Clicks "Deposit Escrow"
    activate UI
    UI->>EscrowFSM: fundMilestone(milestoneId, phone="254712345678")
    activate EscrowFSM
    EscrowFSM->>Daraja: triggerSTKPush(accountRef="CK-MS-881", amount=50000)
    activate Daraja
    Daraja-->>EscrowFSM: CheckoutRequestID
    deactivate Daraja
    
    Note over Client,Daraja: Client approves M-Pesa PIN prompt
    Daraja->>EscrowFSM: Webhook Callback ResultCode=0
    EscrowFSM->>DB: UPDATE tbl_escrow_milestones SET milestone_status='FUNDED_LOCKED' WHERE id=milestoneId
    activate DB
    DB-->>EscrowFSM: Updated
    deactivate DB
    EscrowFSM-->>UI: MilestoneFundedNotification()
    deactivate EscrowFSM
    UI-->>Client: Displays Green Shield "Funds Secured in Regulated Escrow"
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
