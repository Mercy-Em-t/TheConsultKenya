# Sequence Diagram: SQ_UC11 — Process Cross-Border Card Payment
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC11`  
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
    actor Client as 👤 Client (Diaspora / International)
    participant UI as 🖥️ CardPaymentModal
    participant CardCtrl as ⚙️ CardGatewayController
    participant Stripe as 🏛️ International Payment Gateway (3DS)
    participant Ledger as 🗄️ DoubleEntryLedgerService

    Client->>UI: Enters Card Details (Visa/Mastercard)
    activate UI
    UI->>CardCtrl: initiateCardCharge(bookingId, amountUSD=60.00)
    activate CardCtrl
    CardCtrl->>Stripe: createPaymentIntent(amount=6000, currency="usd", 3DSecure="required")
    activate Stripe
    Stripe-->>CardCtrl: {clientSecret, redirect3DSUrl}
    deactivate Stripe
    CardCtrl-->>UI: challenge3DS(redirect3DSUrl)
    UI-->>Client: Displays Bank 3D-Secure SMS OTP Challenge

    Client->>UI: Submits OTP
    UI->>Stripe: confirmPaymentIntent()
    Stripe-->>CardCtrl: Webhook: payment_intent.succeeded (chargeId)
    CardCtrl->>Ledger: postTransaction(debit="STRIPE_SETTLEMENT_USD", credit="CLIENT_DEPOSIT_LIABILITY", amountKes=7800)
    CardCtrl-->>UI: PaymentComplete()
    deactivate CardCtrl
    UI-->>Client: Confirms Booking via Card Payment
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
