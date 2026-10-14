# Sequence Diagram: SQ_UC20 — Moderate Platform Content and Enforce NDAs
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC20`  
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
    actor Admin as 👤 Compliance Moderator
    participant UI as 🖥️ ModerationQueueUI
    participant ModService as ⚙️ ContentModerationService
    participant DB as 🗄️ tbl_case_study_decks

    Admin->>UI: Reviews Flagged Case Study Deck
    activate UI
    UI->>ModService: inspectDeck(deckId)
    activate ModService
    ModService->>DB: queryDeckWithFlags(deckId)
    activate DB
    DB-->>ModService: deckDetails, flaggedClientName
    deactivate DB
    ModService-->>UI: displayReviewPanel()

    Admin->>UI: Selects "Approve with Redaction" & Masks Client Trademark
    UI->>ModService: applyRedaction(deckId, maskedContent)
    ModService->>DB: UPDATE tbl_case_study_decks SET markdown_content=maskedContent, status='PUBLISHED'
    activate DB
    DB-->>ModService: Success
    deactivate DB
    ModService-->>UI: DeckApprovedNotification()
    deactivate ModService
    UI-->>Admin: Updates Queue Status to Cleared
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
