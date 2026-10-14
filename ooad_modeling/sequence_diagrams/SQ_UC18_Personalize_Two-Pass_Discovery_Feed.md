# Sequence Diagram: SQ_UC18 — Personalize Two-Pass Discovery Feed
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC18`  
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
    participant UI as 🖥️ FeedView
    participant RecCtrl as ⚙️ TwoPassEngine (PROG-03)
    participant pgvector as 🗄️ PostgreSQL (HNSW Index)
    participant Redis as ⚡ Redis (CAS Cache)

    Client->>UI: Opens Discovery Tab
    activate UI
    UI->>RecCtrl: getPersonalizedFeed(clientId)
    activate RecCtrl
    
    %% Pass 1
    RecCtrl->>pgvector: SELECT id FROM tbl_case_study_decks ORDER BY embedding <=> clientPrefVector LIMIT 200
    activate pgvector
    pgvector-->>RecCtrl: candidateDeckIds
    deactivate pgvector

    %% Pass 2
    RecCtrl->>Redis: MGET cas_score:authorIds
    activate Redis
    Redis-->>RecCtrl: casScoresList
    deactivate Redis

    RecCtrl->>RecCtrl: computeCompositeRankings()
    RecCtrl->>RecCtrl: applyDiversityFilter(max 2 per author)
    RecCtrl-->>UI: returnTop20Decks()
    deactivate RecCtrl
    UI-->>Client: Renders Infinite Scroll Personalized Feed
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
