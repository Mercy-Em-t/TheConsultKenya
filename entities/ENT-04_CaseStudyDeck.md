# Entity Specification: CaseStudyDeck
**Entity ID:** `ENT-04` | **Category:** Independent Entity (Core Content Kernel)

### Description
A modular, visual-first technical or advisory case study created in Creation Studio. Can exist and be viewed independently within the content catalog.

### Attribute Data Dictionary
| Attribute Name | Data Type | Key / Constraint | Functional Description |
| :--- | :--- | :--- | :--- |
| **`case_study_id`** | `UUID` | PK | Primary surrogate key identifier for the case study. |
| **`author_id`** | `UUID` | FK (ConsultantProfile.consultant_id) | Mandatory author reference. |
| **`case_title`** | `VARCHAR(255)` | Mandatory | Display title of the case study. |
| **`slug`** | `VARCHAR(255)` | Mandatory, Unique | SEO-optimized URI slug. |
| **`executive_summary`** | `TEXT` | Mandatory | Concise problem-solution-impact narrative. |
| **`content_blueprint_json`** | `JSONB` | Mandatory | Structured sections containing markdown, metrics, and Mermaid definitions. |
| **`conversion_anchor_json`** | `JSONB` | Mandatory | Configuration for embedded booking drawer and call-to-action. |
| **`publication_status`** | `ENUM('DRAFT', 'PUBLISHED', 'UNDER_MODERATION', 'REDACTED')` | Mandatory | Lifecycle state. |
| **`view_count`** | `INTEGER` | Mandatory, Default: 0 | Cumulative client view impressions. |
| **`bookmark_count`** | `INTEGER` | Mandatory, Default: 0 | Total times saved to client collections. |
| **`published_at`** | `TIMESTAMPTZ` | Optional | Timestamp when case study was made publicly visible. |

### Relationships & Structural Constraints
| Target Entity | Direction | Cardinality | Modality | Semantic Business Rule |
| :--- | :---: | :---: | :---: | :--- |
| **`ConsultantProfile`** | Child | `(1,1) : 1` | Mandatory | Authored by exactly one ConsultantProfile. |
| **`ExecutionProof`** | Parent | `1 : (0,N)` | Optional | May attach zero or many verifiable ExecutionProofs. |
| **`CaseStudyTagIntersection`** | Parent | `1 : (0,N)` | Optional | Categorized into zero or many TopicTags. |
| **`UserBookmarkIntersection`** | Parent | `1 : (0,N)` | Optional | Bookmarked by zero or many Users. |
