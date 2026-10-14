# Entity Specification: ExecutionProof
**Entity ID:** `ENT-05` | **Category:** Dependent Entity (Characteristic Entity)

### Description
Verifiable evidence item linked to claims in a case study (GitHub commit, live URL, client co-sign, PDF audit memo). Dependent on CaseStudyDeck.

### Attribute Data Dictionary
| Attribute Name | Data Type | Key / Constraint | Functional Description |
| :--- | :--- | :--- | :--- |
| **`proof_id`** | `UUID` | PK | Primary surrogate key identifier for the proof asset. |
| **`case_study_id`** | `UUID` | FK (CaseStudyDeck.case_study_id) | Mandatory reference to parent case study. |
| **`proof_type`** | `ENUM('GITHUB_COMMIT', 'LIVE_URL', 'CLIENT_COSIGN', 'AUDIT_MEMO_PDF')` | Mandatory | Classification of proof. |
| **`external_uri`** | `VARCHAR(500)` | Optional | Direct link to external repository commit or production system. |
| **`sha256_fingerprint`** | `CHAR(64)` | Mandatory | Cryptographic SHA-256 hash verifying asset integrity. |
| **`is_externally_verified`** | `BOOLEAN` | Mandatory, Default: FALSE | Flag set to TRUE upon successful GitHub API or signature validation. |
| **`created_at`** | `TIMESTAMPTZ` | Mandatory | Timestamp of proof registration. |

### Relationships & Structural Constraints
| Target Entity | Direction | Cardinality | Modality | Semantic Business Rule |
| :--- | :---: | :---: | :---: | :--- |
| **`CaseStudyDeck`** | Child | `(1,1) : 1` | Mandatory | Must be attached to exactly one parent CaseStudyDeck. |
