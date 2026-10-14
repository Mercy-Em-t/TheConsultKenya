# Entity Specification: ProfessionalCredential
**Entity ID:** `ENT-03` | **Category:** Dependent Entity (Weak Entity)

### Description
Represents statutory professional certifications (LSK, ICPAK, EBK) and national identity documents submitted for regulatory validation. Dependent on ConsultantProfile.

### Attribute Data Dictionary
| Attribute Name | Data Type | Key / Constraint | Functional Description |
| :--- | :--- | :--- | :--- |
| **`credential_id`** | `UUID` | PK | Primary surrogate key identifier for the credential entry. |
| **`consultant_id`** | `UUID` | FK (ConsultantProfile.consultant_id) | Mandatory reference to owning consultant. |
| **`credential_type`** | `ENUM('NATIONAL_ID', 'KRA_PIN', 'LSK_ADVOCATE', 'ICPAK_CPA', 'EBK_ENGINEER')` | Mandatory | Type of professional board or national credential. |
| **`license_number`** | `VARCHAR(100)` | Mandatory | Official practicing certificate or registration number. |
| **`verification_status`** | `ENUM('PENDING', 'VERIFIED_ACTIVE', 'REJECTED', 'EXPIRED')` | Mandatory | Current verification status from statutory registry. |
| **`registry_response_hash`** | `VARCHAR(64)` | Optional | SHA-256 hash of official API response for immutable audit trail. |
| **`verified_at`** | `TIMESTAMPTZ` | Optional | Timestamp when automated check or compliance officer confirmed validity. |
| **`expiry_date`** | `DATE` | Optional | Statutory expiration date of practicing license. |

### Relationships & Structural Constraints
| Target Entity | Direction | Cardinality | Modality | Semantic Business Rule |
| :--- | :---: | :---: | :---: | :--- |
| **`ConsultantProfile`** | Child | `(1,1) : 1` | Mandatory | Each credential strictly belongs to exactly one ConsultantProfile. |
