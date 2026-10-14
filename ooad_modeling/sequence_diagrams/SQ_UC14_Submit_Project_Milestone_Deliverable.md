# Sequence Diagram: SQ_UC14 — Submit Project Milestone Deliverable
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC14`  
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
    actor Consultant as 👤 Consultant
    participant UI as 🖥️ MilestoneDeliverableUI
    participant EscrowFSM as ⚙️ EscrowStateMachine (PROG-06)
    participant S3 as 🗄️ Amazon S3 Vault
    participant DB as 🗄️ tbl_escrow_milestones

    Consultant->>UI: Attaches Written Legal Opinion PDF & Clicks "Submit Deliverable"
    activate UI
    UI->>EscrowFSM: submitMilestoneDeliverable(milestoneId, fileStream)
    activate EscrowFSM
    EscrowFSM->>EscrowFSM: computeSHA256(fileStream)
    EscrowFSM->>S3: putObject(encryptedFile)
    activate S3
    S3-->>EscrowFSM: fileUri
    deactivate S3
    
    EscrowFSM->>DB: UPDATE tbl_escrow_milestones SET milestone_status='SUBMITTED', deliverable_sha256=hash, submitted_at=NOW()
    activate DB
    DB-->>EscrowFSM: OK
    deactivate DB
    EscrowFSM->>EscrowFSM: start72HourAutoApprovalTimer(milestoneId)
    EscrowFSM-->>UI: SubmissionConfirmed(hash)
    deactivate EscrowFSM
    UI-->>Consultant: Displays Notice: "Deliverable Submitted; 72-hour review window active"
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
