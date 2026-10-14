# Entity Specification: ConsultantProfile
**Entity ID:** `ENT-02` | **Category:** Dependent Entity (Subtype / Characteristic Entity)

### Description
Maintains professional creator profile attributes, authority metrics, and Bento grid modular settings for a consultant. Dependent on UserAccount.

### Attribute Data Dictionary
| Attribute Name | Data Type | Key / Constraint | Functional Description |
| :--- | :--- | :--- | :--- |
| **`consultant_id`** | `UUID` | PK, FK (UserAccount.user_id) | Foreign key referencing parent user and primary key. |
| **`public_handle`** | `VARCHAR(50)` | Mandatory, Unique | URL slug handle (e.g., @kamau_tech) for public routing. |
| **`professional_headline`** | `VARCHAR(200)` | Mandatory | Primary domain expertise tagline (e.g. 'Fintech & eTIMS Architect'). |
| **`cas_score`** | `DECIMAL(6,2)` | Mandatory, Default: 100.00 | Computed Creator Authority Score (0.00 to 1,000.00). |
| **`authority_tier`** | `ENUM('TIER_1_EMERGING', 'TIER_2_ESTABLISHED', 'TIER_3_AUTHORITY')` | Mandatory | Current platform authority classification. |
| **`hourly_rate_kes`** | `DECIMAL(10,2)` | Mandatory | Standard advisory hourly booking rate in Kenyan Shillings. |
| **`bento_grid_layout`** | `JSONB` | Mandatory | Modular widget configuration for public Bento portfolio. |
| **`total_escrow_completed`** | `INTEGER` | Mandatory, Default: 0 | Counter of successfully delivered escrow milestones. |

### Relationships & Structural Constraints
| Target Entity | Direction | Cardinality | Modality | Semantic Business Rule |
| :--- | :---: | :---: | :---: | :--- |
| **`UserAccount`** | Child | `(1,1) : 1` | Mandatory | Each ConsultantProfile must belong to exactly one UserAccount. |
| **`ProfessionalCredential`** | Parent | `1 : (0,N)` | Optional | A ConsultantProfile may hold zero or many ProfessionalCredentials. |
| **`CaseStudyDeck`** | Parent | `1 : (0,N)` | Optional | A ConsultantProfile owns zero or many CaseStudyDecks. |
