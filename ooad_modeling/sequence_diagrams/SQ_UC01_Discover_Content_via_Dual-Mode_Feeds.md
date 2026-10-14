# Sequence Diagram: SQ_UC01 — Discover Content via Dual-Mode Feeds
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC01`  
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
    participant UI as 🖥️ FeedInterface (Boundary)
    participant SearchCtrl as ⚙️ VectorSearchController
    participant Engine as 🧠 TwoPassVectorEngine (PROG-03)
    participant DB as 🗄️ PostgreSQL (pgvector HNSW)
    participant Cache as ⚡ Redis (CAS Multipliers)

    Client->>UI: Selects Topic Hub & Enters Search Query
    activate UI
    UI->>SearchCtrl: getPersonalizedFeed(query, clientContext)
    activate SearchCtrl
    SearchCtrl->>Engine: executeTwoPassRetrieval(queryText, geoTag="KE")
    activate Engine
    
    %% Pass 1
    Engine->>DB: queryCosineHNSW(embedding, topK=200, status='PUBLISHED')
    activate DB
    DB-->>Engine: candidateCardsList (top 200 matches)
    deactivate DB

    %% Pass 2
    Engine->>Cache: mget("cas_score:" + authorIds)
    activate Cache
    Cache-->>Engine: authorCasScoresMap
    deactivate Cache
    
    Engine->>Engine: computeCompositeScore(cosSim, casScore, geoBoost=1.25, freshnessDecay)
    Engine->>Engine: applyAntiSaturationDiversityFilter(max 2 per author in top 20)
    Engine-->>SearchCtrl: rankedCardsTop20
    deactivate Engine

    SearchCtrl-->>UI: renderFeedResponse(cards, nextCursor)
    deactivate SearchCtrl
    UI-->>Client: Displays Visual Cards with playable video teasers
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
