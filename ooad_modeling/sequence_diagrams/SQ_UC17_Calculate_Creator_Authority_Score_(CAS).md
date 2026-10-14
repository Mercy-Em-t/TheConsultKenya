# Sequence Diagram: SQ_UC17 — Calculate Creator Authority Score (CAS)
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC17`  
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
    participant Cron as ⏰ HourlyBatchDaemon
    participant CASEngine as 🧠 CASEngine (PROG-03)
    participant DB as 🗄️ PostgreSQL Database
    participant Redis as ⚡ Redis Cache

    Cron->>CASEngine: triggerHourlyCASRecalculation()
    activate CASEngine
    CASEngine->>DB: queryConsultantsWithRecentActivity()
    activate DB
    DB-->>CASEngine: consultantList
    deactivate DB

    loop For each consultant
        CASEngine->>CASEngine: C_cred = credentialVerificationWeight (0-400)
        CASEngine->>CASEngine: C_perf = completedSessionsWeight (0-300)
        CASEngine->>CASEngine: C_eval = clientRatingsWeight (0-200)
        CASEngine->>CASEngine: C_eng  = caseStudyDwellWeight (0-100)
        CASEngine->>CASEngine: CAS_total = C_cred + C_perf + C_eval + C_eng
        CASEngine->>Redis: SET "cas_score:" + consultantId CAS_total
        CASEngine->>DB: UPDATE tbl_consultant_profiles SET authority_score = CAS_total
    end

    CASEngine-->>Cron: BatchCompleted(count)
    deactivate CASEngine
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
