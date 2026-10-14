# Entity Specification: EscrowMilestone
**Entity ID:** `ENT-11` | **Category:** Dependent Entity (Sub-Contract Tranche Entity)

### Description
An atomic phase within an EscrowContract with specific deliverables, due date, inspection timer, and escrow release sum. Dependent on EscrowContract.

### Attribute Data Dictionary
| Attribute Name | Data Type | Key / Constraint | Functional Description |
| :--- | :--- | :--- | :--- |
| **`milestone_id`** | `UUID` | PK | Primary surrogate key identifier for the milestone. |
| **`contract_id`** | `UUID` | FK (EscrowContract.contract_id) | Mandatory reference to parent contract. |
| **`sequence_number`** | `SMALLINT` | Mandatory | Sequential order (e.g. 1, 2, 3) of milestone. |
| **`milestone_title`** | `VARCHAR(150)` | Mandatory | Descriptive phase name (e.g. 'Architecture Blueprint'). |
| **`milestone_amount_kes`** | `DECIMAL(12,2)` | Mandatory | Principal amount locked in escrow for this tranche. |
| **`milestone_status`** | `ENUM('PENDING_FUNDING', 'FUNDED_LOCKED', 'SUBMITTED', 'REVISIONS_REQUESTED', 'APPROVED_RELEASED', 'FROZEN_DISPUTE')` | Mandatory | State of the milestone. |
| **`deliverable_sha256`** | `CHAR(64)` | Optional | Cryptographic fingerprint of submitted artifacts. |
| **`inspection_deadline`** | `TIMESTAMPTZ` | Optional | 72-hour auto-approval deadline timestamp. |
| **`approved_at`** | `TIMESTAMPTZ` | Optional | Timestamp when funds were authorized for release. |

### Relationships & Structural Constraints
| Target Entity | Direction | Cardinality | Modality | Semantic Business Rule |
| :--- | :---: | :---: | :---: | :--- |
| **`EscrowContract`** | Child | `(1,1) : 1` | Mandatory | Belongs strictly to exactly one EscrowContract. |
| **`DisputeCase`** | Parent | `1 : (0,1)` | Optional | May be subject to zero or one DisputeCase. |
| **`LedgerTransaction`** | Parent | `1 : (1,N)` | Mandatory | Produces one or many LedgerTransactions. |
