# Sequence Diagram: SQ_UC19 — Manage Phased Rollout and Creator Onboarding
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC19`  
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
    actor Admin as 👤 Platform Admin
    participant UI as 🖥️ AdminConsoleUI
    participant RolloutMgr as ⚙️ RolloutManagerService
    participant DB as 🗄️ tbl_system_configurations

    Admin->>UI: Selects "Activate Phase B (Mombasa & Kisumu)"
    activate UI
    UI->>RolloutMgr: transitionRolloutPhase(newPhase="PHASE_B_COASTAL_WESTERN")
    activate RolloutMgr
    RolloutMgr->>RolloutMgr: verifyPilotExitCriteriaMet()
    RolloutMgr->>DB: UPDATE tbl_system_configurations SET active_rollout_phase = 'PHASE_B'
    activate DB
    DB-->>RolloutMgr: Updated
    deactivate DB
    RolloutMgr-->>UI: RolloutPhaseActivated()
    deactivate RolloutMgr
    UI-->>Admin: Confirms Regional Geofences Opened
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
