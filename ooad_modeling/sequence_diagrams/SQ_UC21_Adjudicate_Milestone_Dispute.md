# Sequence Diagram: SQ_UC21 — Adjudicate Milestone Dispute
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC21`  
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
    actor Mediator as 👤 Chartered Arbitrator (CIArb)
    participant UI as 🖥️ ArbitratorConsoleUI
    participant AdjEngine as ⚙️ DisputeAdjudicationEngine (PROG-08)
    participant EscrowFSM as ⚙️ EscrowStateMachine (PROG-06)
    participant Daraja as 🏛️ Safaricom Daraja B2C
    participant DB as 🗄️ tbl_dispute_cases

    Mediator->>UI: Reviews Evidence Dossier (Claimant & Respondent PDF Uploads)
    activate UI
    Mediator->>UI: Submits Binding Award: 60% Client Refund, 40% Consultant Payout
    UI->>AdjEngine: executeMediatorRuling(caseId, clientPct=60.0, consultantPct=40.0, justification)
    activate AdjEngine
    
    AdjEngine->>AdjEngine: validateSplitSumEquals100(clientPct, consultantPct)
    AdjEngine->>AdjEngine: generateAdjudicationCertificate(caseId, SHA256Seal)
    
    %% Split Disbursements
    AdjEngine->>EscrowFSM: executeDisputeSplitRelease(milestoneId, clientAmount=30000, consultantAmount=20000)
    activate EscrowFSM
    EscrowFSM->>Daraja: triggerB2CRefund(phone=clientPhone, amount=30000)
    EscrowFSM->>Daraja: triggerB2CPayout(phone=consultantPhone, amount=17600 [net])
    EscrowFSM->>EscrowFSM: transitionTo("CLOSED_DISPUTE_RESOLVED")
    EscrowFSM-->>AdjEngine: SplitComplete
    deactivate EscrowFSM

    AdjEngine->>DB: UPDATE tbl_dispute_cases SET status='CLOSED_RESOLVED', certificate_url=certUrl
    activate DB
    DB-->>AdjEngine: Closed
    deactivate DB
    AdjEngine-->>UI: RulingExecutedSuccessfully(certUrl)
    deactivate AdjEngine
    UI-->>Mediator: Displays Signed Binding Arbitration Certificate
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
