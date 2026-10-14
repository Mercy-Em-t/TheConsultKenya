# Entity Specification: EscrowContract
**Entity ID:** `ENT-10` | **Category:** Independent / Operational Contract Entity

### Description
Represents a formal Statement of Work (SOW) consulting agreement or high-value advisory engagement with funds held in trust across defined milestones.

### Attribute Data Dictionary
| Attribute Name | Data Type | Key / Constraint | Functional Description |
| :--- | :--- | :--- | :--- |
| **`contract_id`** | `UUID` | PK | Primary surrogate key identifier for the escrow contract. |
| **`client_id`** | `UUID` | FK (UserAccount.user_id) | Mandatory hiring client reference. |
| **`consultant_id`** | `UUID` | FK (ConsultantProfile.consultant_id) | Mandatory delivering consultant reference. |
| **`contract_title`** | `VARCHAR(200)` | Mandatory | Formal title of Statement of Work. |
| **`contract_status`** | `ENUM('DRAFT', 'FUNDED_ACTIVE', 'IN_DISPUTE', 'COMPLETED_RELEASED', 'REFUNDED')` | Mandatory | Lifecycle state. |
| **`total_contract_value_kes`** | `DECIMAL(12,2)` | Mandatory | Aggregated value of all milestone tranches in KES. |
| **`platform_commission_rate`** | `DECIMAL(4,4)` | Mandatory, Default: 0.0700 | Platform take rate (e.g. 7.00%). |
| **`created_at`** | `TIMESTAMPTZ` | Mandatory | Timestamp when contract was drafted. |

### Relationships & Structural Constraints
| Target Entity | Direction | Cardinality | Modality | Semantic Business Rule |
| :--- | :---: | :---: | :---: | :--- |
| **`UserAccount`** | Child | `(1,1) : 1` | Mandatory | Contracted by exactly one Client. |
| **`ConsultantProfile`** | Child | `(1,1) : 1` | Mandatory | Delivered by exactly one Consultant. |
| **`EscrowMilestone`** | Parent | `1 : (1,N)` | Mandatory | Composed of one or many EscrowMilestones. |
| **`DisputeCase`** | Parent | `1 : (0,N)` | Optional | May have zero or many DisputeCases. |
