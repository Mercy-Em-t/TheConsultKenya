# Entity Specification: UserBookmarkIntersection
**Entity ID:** `ENT-08` | **Category:** Intersection Entity (Associative Entity: M:N Resolver)

### Description
Resolves the Many-to-Many (M:N) relationship between UserAccount and CaseStudyDeck for saved collections. Emits high-value 5x algorithmic signals.

### Attribute Data Dictionary
| Attribute Name | Data Type | Key / Constraint | Functional Description |
| :--- | :--- | :--- | :--- |
| **`user_id`** | `UUID` | PK, FK (UserAccount.user_id) | Foreign key referencing saving user. |
| **`case_study_id`** | `UUID` | PK, FK (CaseStudyDeck.case_study_id) | Foreign key referencing saved case study. |
| **`collection_name`** | `VARCHAR(100)` | Mandatory, Default: 'Default' | User-defined named collection folder. |
| **`saved_at`** | `TIMESTAMPTZ` | Mandatory | Timestamp when bookmark was saved. |

### Relationships & Structural Constraints
| Target Entity | Direction | Cardinality | Modality | Semantic Business Rule |
| :--- | :---: | :---: | :---: | :--- |
| **`UserAccount`** | Child | `(1,1) : 1` | Mandatory | Saved by exactly one UserAccount. |
| **`CaseStudyDeck`** | Child | `(1,1) : 1` | Mandatory | Points to exactly one CaseStudyDeck. |
