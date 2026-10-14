# Use Case Specification: Bookmark & Organize Case Studies
**Use Case Name:** Bookmark & Organize Case Studies | **ID:** `UC-04` | **Priority:** Medium

**Actor:** Client / Enterprise Buyer
**Description:** The Client bookmarks case studies, technical blueprints, or checklists into custom private or team collections. Bookmarks signal high intent to the algorithmic discovery engine.
**Trigger:** Client clicks the bookmark/save icon on a case study card or deck.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Client is authenticated.
2. Case study is active and accessible.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Save case study to organized collection |  | Bookmark Action |
| **1** | Client clicks 'Bookmark' icon on a case study card | $\longleftarrow$ | Bookmark trigger |
| **2** | System displays modal with existing collections and '+ New Collection' option | $\longrightarrow$ | Collection list modal |
| **3** | Client chooses target collection (e.g., 'Q3 Tech Stack Architecture') | $\longleftarrow$ | Selected Collection ID |
| **4** | System saves bookmark record into User Collections datastore | $\longrightarrow$ | Bookmark Record |
| **5** | System emits high-weight algorithmic event (5x save multiplier) to CAS engine for creator | $\longrightarrow$ | Algorithmic save signal |
| **6** | System presents confirmation toast: 'Saved to Q3 Tech Stack Architecture' | $\longrightarrow$ | Confirmation toast |

#### Alternative Courses
**4.1 Client creates a new collection on the fly (branch at step 3)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Client enters new collection name and privacy toggle (Private / Team Shared) | $\longleftarrow$ | New collection metadata |
| 2a | System creates new collection entity and adds selected case study | $\longrightarrow$ | Created collection entity |
| 3a | System proceeds to step 5 of Normal Course |  | Resume workflow |

### Postconditions
1. Case study is accessible in client's Saved library.
2. Creator's case study save tally incremented by 1.

### Exceptions
**E1: Duplicate bookmark attempted**
1. System alerts: 'Already in collection. Would you like to move or remove?'
2. Client can un-bookmark or cancel without error.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Case Study ID & Collection selection | Client Input | Updated Bookmark Record | User Collections Database |
| Existing collections list | User Profile Datastore | 5x CAS Engagement Signal | Recommendation Pipeline |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-004 (Bookmark & Collection Management), FR-017 (CAS Telemetry Tracking)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-04-01: Verify bookmarking persists across page reloads and mobile apps.`
- **Boundary & Alternative Test Cases:**
  - `TC-04-02: Test maximum collection name length (100 chars) and 500+ bookmarks in a single folder.`
- **Negative & Exception Test Cases:**
  - `TC-04-03: Verify handling of bookmarked case studies if creator deletes or unpublishes deck.`
