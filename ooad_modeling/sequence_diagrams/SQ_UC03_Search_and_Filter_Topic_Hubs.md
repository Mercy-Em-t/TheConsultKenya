# Sequence Diagram: SQ_UC03 — Search and Filter Topic Hubs
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC03`  
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
    participant UI as 🖥️ SearchHubUI
    participant FilterCtrl as ⚙️ TopicFilterController
    participant DB as 🗄️ PostgreSQL Database

    Client->>UI: Selects Industry Filter ("Tax Compliance") & Price Range
    activate UI
    UI->>FilterCtrl: filterHub(topicSlug="tax-compliance", minRate, maxRate)
    activate FilterCtrl
    FilterCtrl->>DB: executeFilteredSearch(slug, rates, verifiedOnly=True)
    activate DB
    DB-->>FilterCtrl: matchingConsultantsList
    deactivate DB
    FilterCtrl-->>UI: displayResults(matchingConsultantsList)
    deactivate FilterCtrl
    UI-->>Client: Displays Filtered Results with Active Badges
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
