# Sequence Diagram: SQ_UC02 — Inspect Consultant Portfolio Bento Grid
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC02`  
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
    participant UI as 🖥️ BentoGridUI (Boundary)
    participant ProfileCtrl as ⚙️ ConsultantProfileController
    participant Consultant as 🏛️ ConsultantProfile (Domain)
    participant DB as 🗄️ PostgreSQL Database

    Client->>UI: Clicks Consultant Profile (e.g. Adv. Mutua)
    activate UI
    UI->>ProfileCtrl: getBentoGridProfile(consultantId)
    activate ProfileCtrl
    ProfileCtrl->>DB: queryProfileWithProof(consultantId)
    activate DB
    DB-->>ProfileCtrl: consultantRecord, verifiedBadges, caseStudies
    deactivate DB

    ProfileCtrl->>Consultant: constructBentoView()
    activate Consultant
    Consultant-->>ProfileCtrl: bentoGridPayload (Hero, Metrics, Evidence, Rates)
    deactivate Consultant

    ProfileCtrl-->>UI: returnBentoJson(bentoGridPayload)
    deactivate ProfileCtrl
    UI-->>Client: Renders Interactive Modular Bento Layout
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
