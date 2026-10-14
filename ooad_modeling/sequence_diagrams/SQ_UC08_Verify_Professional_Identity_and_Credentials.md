# Sequence Diagram: SQ_UC08 — Verify Professional Identity and Credentials
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC08`  
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
    participant UI as 🖥️ VerificationUI
    participant AuthCtrl as ⚙️ AuthVerificationService (PROG-01)
    participant RegAdapter as 🏛️ StatutoryRegistryAdapter
    participant DB as 🗄️ PostgreSQL Database
    participant Celery as ⚡ Celery Worker

    Consultant->>UI: Submits National ID & Practising License (e.g. LSK P.105/...)
    activate UI
    UI->>AuthCtrl: verifyCredentials(consultantId, licenseNo, board="LSK_ADVOCATE")
    activate AuthCtrl
    AuthCtrl->>RegAdapter: queryActiveStanding("LSK_ADVOCATE", licenseNo)
    activate RegAdapter
    
    alt Registry Responds Active
        RegAdapter-->>AuthCtrl: {isActive: true, fullName: "Mutua James", rollDate: "2014"}
        AuthCtrl->>DB: UPDATE tbl_consultant_profiles SET verification_status='VERIFIED_ACTIVE', authority_tier='TIER_3_AUTHORITY'
        activate DB
        DB-->>AuthCtrl: Updated
        deactivate DB
        AuthCtrl->>Celery: enqueue("RecalculateCreatorAuthorityScore", consultantId)
        AuthCtrl-->>UI: VerificationSuccess (tier="TIER_3_AUTHORITY")
    else Registry Mismatch or Inactive
        RegAdapter-->>AuthCtrl: {isActive: false, reason: "License Expired"}
        AuthCtrl->>DB: UPDATE tbl_consultant_profiles SET verification_status='REJECTED'
        AuthCtrl-->>UI: VerificationRejected ("License expired with statutory body")
    end
    deactivate RegAdapter
    deactivate AuthCtrl
    UI-->>Consultant: Displays Badge Status Update
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
