# Entity Specification: LedgerTransaction
**Entity ID:** `ENT-12` | **Category:** Dependent Entity (Immutable Financial Double-Entry Record)

### Description
An immutable double-entry journal entry tracking money movement across payment rails, platform commission, trust escrow, and B2C payouts. Dependent on Booking or Milestone.

### Attribute Data Dictionary
| Attribute Name | Data Type | Key / Constraint | Functional Description |
| :--- | :--- | :--- | :--- |
| **`transaction_id`** | `UUID` | PK | Primary surrogate key identifier for the ledger row. |
| **`booking_id`** | `UUID` | Optional, FK (ConsultationBooking.booking_id) | Optional reference to consultation booking. |
| **`milestone_id`** | `UUID` | Optional, FK (EscrowMilestone.milestone_id) | Optional reference to escrow milestone. |
| **`debit_account`** | `VARCHAR(50)` | Mandatory | Double-entry debit account (e.g., 'ESCROW_TRUST_CASH', 'CLIENT_FUNDS'). |
| **`credit_account`** | `VARCHAR(50)` | Mandatory | Double-entry credit account (e.g., 'CONSULTANT_PAYABLE', 'PLATFORM_REVENUE'). |
| **`amount_kes`** | `DECIMAL(12,2)` | Mandatory | Exact monetary amount in Kenyan Shillings. |
| **`payment_rail`** | `ENUM('MPESA_DARAYA', 'CARD_PAYSTACK', 'RTGS_WIRE', 'MPESA_B2C')` | Mandatory | Fintech rail utilized. |
| **`external_reference`** | `VARCHAR(100)` | Mandatory, Unique | Safaricom M-Pesa receipt code or bank transaction reference. |
| **`etims_invoice_number`** | `VARCHAR(100)` | Optional | KRA eTIMS statutory tax invoice code. |
| **`created_at`** | `TIMESTAMPTZ` | Mandatory | Immutable timestamp when entry was recorded. |

### Relationships & Structural Constraints
| Target Entity | Direction | Cardinality | Modality | Semantic Business Rule |
| :--- | :---: | :---: | :---: | :--- |
| **`ConsultationBooking`** | Child | `(0,1) : 1` | Optional | Linked to at most one ConsultationBooking. |
| **`EscrowMilestone`** | Child | `(0,1) : 1` | Optional | Linked to at most one EscrowMilestone. |
