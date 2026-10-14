# Sequence Diagram: SQ_UC09 — Book In-App Advisory Consultation
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC09`  
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
    participant UI as 🖥️ BookingCalendarUI
    participant SlotMgr as ⚙️ SlotLockManager (PROG-04)
    participant Redis as ⚡ Redis Lock Store
    participant DB as 🗄️ tbl_consultation_bookings

    Client->>UI: Taps Available Slot (Thursday 14:00 EAT)
    activate UI
    UI->>SlotMgr: acquireAdvisorySlotLock(clientId, consultantId, startTime)
    activate SlotMgr
    
    SlotMgr->>Redis: SET slot_lock:consultantId:startTime lockToken NX EX 900
    activate Redis
    
    alt Lock Acquired (Key did not exist)
        Redis-->>SlotMgr: OK (1)
        deactivate Redis
        SlotMgr->>DB: INSERT INTO tbl_consultation_bookings (status='PENDING_PAYMENT', lockToken)
        activate DB
        DB-->>SlotMgr: bookingId (UUID)
        deactivate DB
        SlotMgr-->>UI: LockSuccess (token, ttl=900, bookingId)
        UI-->>Client: Opens Checkout Drawer with 15-Minute Countdown (14:59)
    else Slot Contention (Collision)
        SlotMgr-->>UI: LockFailed ("Slot currently reserved by another client")
        UI-->>Client: Displays Toast: "Slot just taken, please select another time"
    end
    deactivate SlotMgr
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
