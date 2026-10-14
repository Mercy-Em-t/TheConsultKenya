# Sequence Diagram: SQ_UC16 — Initiate Escrow Dispute and Mediation
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC16`  
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
    participant UI as 🖥️ DisputeModalUI
    participant DisputeCtrl as ⚙️ DisputeController (PROG-08)
    participant EscrowFSM as ⚙️ EscrowStateMachine (PROG-06)
    participant DB as 🗄️ tbl_dispute_cases

    Client->>UI: Clicks "Lodge Formal Dispute" (within 7 days of submission)
    activate UI
    UI->>DisputeCtrl: fileDispute(milestoneId, reason="DEFICIENT_DELIVERABLE", evidenceFiles)
    activate DisputeCtrl
    
    DisputeCtrl->>EscrowFSM: freezeMilestoneForDispute(milestoneId)
    activate EscrowFSM
    EscrowFSM->>EscrowFSM: transitionTo("FROZEN_DISPUTE")
    EscrowFSM-->>DisputeCtrl: FrozenConfirmed
    deactivate EscrowFSM

    DisputeCtrl->>DB: INSERT INTO tbl_dispute_cases (status='OPEN_PENDING_REBUTTAL', deadline=NOW()+48h)
    activate DB
    DB-->>DisputeCtrl: caseId (UUID)
    deactivate DB

    DisputeCtrl-->>UI: DisputeLodgedReceipt(caseId, rebuttalDeadline)
    deactivate DisputeCtrl
    UI-->>Client: Displays Confirmation: "Milestone Frozen; Consultant has 48h to respond"
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
