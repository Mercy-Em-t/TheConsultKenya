# Use Case Specification: Search & Filter Topic Hubs
**Use Case Name:** Search & Filter Topic Hubs | **ID:** `UC-03` | **Priority:** High

**Actor:** Client / Enterprise Buyer
**Description:** The Client searches for specialized advisors, legal/financial expertise, or technical case studies using natural language queries, keyword tags, or structured filters (e.g., industry, pricing tier, verified board membership).
**Trigger:** Client enters a search query in the search bar or selects a topic category hub.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Search index and vector embeddings are up to date.
2. Minimum query length is 2 characters or valid tag filter selected.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Perform semantic and structured topic search |  | Search Execution |
| **1** | Client types search query (e.g. 'eTIMS system integration Kenya') or selects topic badge | $\longleftarrow$ | Raw query string / Tag ID |
| **2** | System executes Pass-1 candidate retrieval across full-text index and vector embedding store | $\longleftarrow$ | Vector Cosine Search |
| **3** | System retrieves matching case studies, verified consultants, and discussion threads | $\longleftarrow$ | Candidate hit set |
| **4** | System ranks results applying Creator Authority Scores and relevance thresholds | $\longleftarrow$ | CAS Scored Ranking |
| **5** | System presents segmented search result view: [Top Consultants | Relevant Case Studies | Topic Tags] | $\longrightarrow$ | Segmented Search Results View |
| **6** | Client applies facet filters (Hourly Rate: KES 5,000-15,000, LSK Certified, Rating > 4.8) | $\longleftarrow$ | Facet filter criteria |
| **7** | System re-renders filtered list instantaneously (<100ms via client-side cache) | $\longrightarrow$ | Refined result list |

#### Alternative Courses
**3.1 No direct matches found (Zero Results Query)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | System detects zero candidate matches | $\longleftarrow$ | Empty hit set |
| 2a | System provides phonetic 'Did you mean?' suggestions and related topic hubs | $\longrightarrow$ | Fuzzy suggestions & related hubs |
| 3a | Client selects recommended alternative hub | $\longleftarrow$ | Alternative hub selection |
| 4a | System resumes Normal Course at step 5 |  | Resume workflow |

### Postconditions
1. Search telemetry logged for keyword trend analysis.
2. Client search history cached locally for instant revisit.

### Exceptions
**E1: Vector search engine timeout**
1. System falls back automatically to PostgreSQL full-text search (tsvector).
2. Results served with non-blocking warning flag.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Query string and facet filters | Client Search Input | Segmented Search Results UI | Client Display |
| Vector embeddings & Full-text index | Elasticsearch / pgvector Datastore | Query telemetry log | Platform Search Analytics |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-003 (Semantic Search & Filtering), FR-018 (Two-Pass Retrieval)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-03-01: Verify natural language query 'KRA audit tax consultant' returns top-3 LSK/ICPAK certified experts.`
- **Boundary & Alternative Test Cases:**
  - `TC-03-02: Test query with special characters, emojis, and maximum string length (256 chars).`
- **Negative & Exception Test Cases:**
  - `TC-03-03: Verify graceful fallback to SQL LIKE search when vector store latency exceeds 300ms.`
