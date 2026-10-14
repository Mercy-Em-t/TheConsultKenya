# Entity Specification: CaseStudyTagIntersection
**Entity ID:** `ENT-07` | **Category:** Intersection Entity (Associative Entity: M:N Resolver)

### Description
Resolves the Many-to-Many (M:N) relationship between CaseStudyDeck and TopicTag. Contains composite foreign keys and ranking relevance weight.

### Attribute Data Dictionary
| Attribute Name | Data Type | Key / Constraint | Functional Description |
| :--- | :--- | :--- | :--- |
| **`case_study_id`** | `UUID` | PK, FK (CaseStudyDeck.case_study_id) | Foreign key referencing case study. |
| **`tag_id`** | `UUID` | PK, FK (TopicTag.tag_id) | Foreign key referencing topic tag. |
| **`relevance_score`** | `DECIMAL(4,3)` | Mandatory, Default: 1.000 | Semantic affinity weight between tag and deck. |
| **`assigned_at`** | `TIMESTAMPTZ` | Mandatory | Timestamp when tag association was created. |

### Relationships & Structural Constraints
| Target Entity | Direction | Cardinality | Modality | Semantic Business Rule |
| :--- | :---: | :---: | :---: | :--- |
| **`CaseStudyDeck`** | Child | `(1,1) : 1` | Mandatory | Connects to one CaseStudyDeck. |
| **`TopicTag`** | Child | `(1,1) : 1` | Mandatory | Connects to one TopicTag. |
