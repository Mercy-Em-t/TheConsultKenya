# Sequence Diagram: SQ_UC22 — Audit Financial Settlement and Tax Compliance
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC22`  
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
    actor Auditor as 👤 Financial Auditor / KRA Inspector
    participant UI as 🖥️ TaxAuditPortalUI
    participant AuditService as ⚙️ FinancialTaxAuditService
    participant DB as 🗄️ tbl_tax_invoices
    participant KRA as 🏛️ KRA eTIMS Verification Portal

    Auditor->>UI: Enters Date Range (October 2026) & Clicks "Generate Tax Schedule"
    activate UI
    UI->>AuditService: generateMonthlyTaxAuditReport(startDate, endDate)
    activate AuditService
    AuditService->>DB: queryInvoicesWithLedgerJournals(startDate, endDate)
    activate DB
    DB-->>AuditService: recordsList (Gross, Fee, VAT, WHT, ControlCodes)
    deactivate DB

    AuditService->>AuditService: reconcileLedgerTotals(Debits == Credits)
    AuditService->>KRA: batchVerifyControlCodes(sample100Codes)
    activate KRA
    KRA-->>AuditService: All 100 Signatures Validated Active
    deactivate KRA

    AuditService-->>UI: returnAuditReport(summarySchedule, reconciliationDiff=0.00)
    deactivate AuditService
    UI-->>Auditor: Renders Official Statutory W2 / VAT-3 Withholding Tax Schedule
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
