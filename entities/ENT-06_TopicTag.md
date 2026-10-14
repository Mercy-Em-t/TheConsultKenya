# Entity Specification: TopicTag
**Entity ID:** `ENT-06` | **Category:** Independent Entity (Lookup / Taxonomy Entity)

### Description
Standardized taxonomy keywords and industry classifications (e.g., #FintechCompliance, #KRAeTIMS, #SoftwareArchitecture) used for two-pass discovery indexing.

### Attribute Data Dictionary
| Attribute Name | Data Type | Key / Constraint | Functional Description |
| :--- | :--- | :--- | :--- |
| **`tag_id`** | `UUID` | PK | Primary surrogate key identifier for the topic tag. |
| **`tag_name`** | `VARCHAR(60)` | Mandatory, Unique | Display keyword hashtag without spaces. |
| **`category_domain`** | `VARCHAR(60)` | Mandatory | Broader professional domain (e.g., Legal, Tax, Engineering). |
| **`is_featured`** | `BOOLEAN` | Mandatory, Default: FALSE | Flag indicating prominent home feed placement. |

### Relationships & Structural Constraints
| Target Entity | Direction | Cardinality | Modality | Semantic Business Rule |
| :--- | :---: | :---: | :---: | :--- |
| **`CaseStudyTagIntersection`** | Parent | `1 : (0,N)` | Optional | Applied to zero or many CaseStudyDecks. |
