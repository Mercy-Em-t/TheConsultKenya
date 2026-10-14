# Use Case Specification: Discover Content via Dual-Mode Feeds
**Use Case Name:** Discover Content via Dual-Mode Feeds | **ID:** `UC-01` | **Priority:** High

**Actor:** Client / Enterprise Buyer (also Guest Visitor)
**Description:** The Client accesses the Consult Kenya discovery feed to explore authoritative business and technical case studies through either a vertical TikTok-style micro-feed or a curated horizontal topic carousel. The system tailors the feed using Creator Authority Scores (CAS) and engagement telemetry.
**Trigger:** Client launches mobile/web app or navigates to the home feed to discover domain insights.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Client device has network connectivity or cached local feed state.
2. Recommendation engine and vector database are operational.
3. Case study repository contains verified published decks.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Browse dual-mode discovery feed |  | Feed Initialization |
| **1** | Client opens home feed and selects preferred viewing mode (Vertical Feed vs. Horizontal Carousels) | $\longleftarrow$ | Feed mode preference (swipe / grid) |
| **2** | System queries recommendation engine with client persona, topic history, and geo-filter (East Africa / Kenya) | $\longleftarrow$ | Client session profile & geo-tag |
| **3** | System ranks published case studies using CAS weight and engagement decay | $\longleftarrow$ | Scored case study candidate list |
| **4** | System streams first page of case study previews (video snippet, title, author Bento card, metrics) | $\longrightarrow$ | Ranked feed card array |
| **5** | Client scrolls or swipes through cards, dwelling on specific case study | $\longleftarrow$ | Dwell time telemetry & interaction event |
| **6** | System records dwell telemetry and dynamically pre-buffers full case study assets (Mermaid charts, proofs) | $\longrightarrow$ | Pre-buffered case study deck |
| **7** | Client taps card to expand full case study presentation | $\longleftarrow$ | Card expansion selection |
| **8** | System renders interactive case study with author conversion CTA anchor | $\longrightarrow$ | Full interactive case study view |

#### Alternative Courses
**1.1 Client filters by specific industry topic or hashtag (branch at step 1)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Client selects topic filter badge (e.g. #FintechCompliance, #KRAeTIMS, #AgriTech) | $\longleftarrow$ | Selected topic tag |
| 2a | System queries vector engine filtered strictly by requested taxonomy | $\longleftarrow$ | Taxonomy query filter |
| 3a | System renders topic-focused sub-feed sorted by CAS rating | $\longrightarrow$ | Topic-filtered case study array |
| 4a | System resumes Normal Course at step 5 |  | Resume workflow |

**1.2 Offline / low-bandwidth fallback (branch at step 2)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | System detects network degradation (<50 kbps or offline) | $\longleftarrow$ | Network latency status |
| 2a | System serves locally cached lightweight SQLite summary cards without rich video | $\longrightarrow$ | Cached summary cards |
| 3a | System queues user interaction events into local IndexedDB for delayed sync | $\longrightarrow$ | Queued telemetry log |

### Postconditions
1. Client view history is updated in the telemetry database.
2. Creator of the viewed case study receives dwell-time impression signal.
3. Client session state preserves feed scroll position.

### Exceptions
**E1: Feed generation timeout or service unavailability (occurs at step 3)**
1. System displays graceful fallback message: 'Live recommendation unavailable. Loading trending case studies.'
2. System serves static cached trending leaderboard.
3. System logs warning to platform telemetry aggregator.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Client session profile & mode toggle | Client Browser / Mobile App | Ranked Feed Card Stream | Client Display UI |
| Case study index & CAS weights | Recommendation Database / Redis Cache | Pre-buffered Case Study Deck | Client Memory Store |
| Dwell time telemetry | Client Telemetry Tracker | Impression & Dwell Telemetry | Analytics Logging Engine |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-001 (Content Ingestion & Delivery), FR-018 (Algorithmic Feed Personalization), FR-022 (Offline Caching)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-01-01: Verify default personalized dual-mode feed renders within 800ms.`
  - `TC-01-02: Verify switching to horizontal carousel preserves current focus.`
- **Boundary & Alternative Test Cases:**
  - `TC-01-03: Verify feed performance with 10,000+ cached items under slow 3G network.`
- **Negative & Exception Test Cases:**
  - `TC-01-04: Verify recommendation engine outage triggers cached trending fallback.`
