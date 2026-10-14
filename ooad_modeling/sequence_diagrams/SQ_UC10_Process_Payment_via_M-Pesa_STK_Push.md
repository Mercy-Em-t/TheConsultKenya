# Sequence Diagram: SQ_UC10 — Process Payment via M-Pesa STK Push
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC10`  
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
    participant UI as 🖥️ CheckoutDrawerUI
    participant PayCoord as ⚙️ MpesaDarajaCoordinator (PROG-05)
    participant Daraja as 🏛️ Safaricom Daraja API
    participant Redis as ⚡ Redis (Idempotency)
    participant Ledger as 🗄️ DoubleEntryLedgerService

    Client->>UI: Enters M-Pesa Phone (0712345678) & Clicks "Pay KES 7,500"
    activate UI
    UI->>PayCoord: initiateSTKPush(bookingId, phone, amount=7500)
    activate PayCoord
    PayCoord->>Daraja: POST /mpesa/stkpush/v1/processrequest (Password, Passkey, Timestamp)
    activate Daraja
    Daraja-->>PayCoord: {ResponseCode: "0", CheckoutRequestID: "ws_CO_88192"}
    deactivate Daraja
    PayCoord-->>UI: STKPromptDispatched (waitingForPin=True)
    UI-->>Client: Displays Phone Prompt Alert: "Enter PIN on your phone"

    Note over Client,Daraja: Client enters PIN on Safaricom SIM Toolkit

    Daraja->>PayCoord: POST /api/v1/payments/mpesa/callback (CheckoutRequestID, ResultCode=0, Receipt="QHD78129KJ")
    PayCoord->>Redis: SET processed_daraja:ws_CO_88192 "QHD78129KJ" NX EX 259200
    activate Redis
    Redis-->>PayCoord: OK (First time processed)
    deactivate Redis

    PayCoord->>Ledger: postTransaction(debit="ESCROW_TRUST_CASH", credit="CLIENT_DEPOSIT_LIABILITY", amount=7500)
    PayCoord->>PayCoord: updateBookingStatus(bookingId, "CONFIRMED_ESCROW_LOCKED")
    PayCoord->>Redis: DEL slot_lock:consultantId:startTime
    PayCoord-->>UI: WebSocketNotification("PAYMENT_SUCCESS", receipt="QHD78129KJ")
    UI-->>Client: Screen Transitions to "Booking Confirmed & Calendar Invite Dispatched"
    deactivate PayCoord
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
