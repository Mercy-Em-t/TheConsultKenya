# Use Case Specification: Personalize Two-Pass Discovery Feed
**Use Case Name:** Personalize Two-Pass Discovery Feed | **ID:** `UC-18` | **Priority:** High

**Actor:** Automated System Daemon
**Description:** The AI recommendation engine executes a two-pass algorithm to serve ultra-relevant, authoritative content to every user. Pass 1 conducts high-speed candidate retrieval via vector embeddings; Pass 2 performs heavy business re-ranking incorporating CAS scores, geographic relevance (Kenya/East Africa), and personal interest.
**Trigger:** External request from UC-01 (client loading feed) or client session update.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Vector embedding store (pgvector/Pinecone) is indexed.
2. Pre-computed CAS weights available in Redis.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Execute two-pass candidate retrieval and ranking |  | Feed Personalization |
| **1** | Recommendation worker receives client request with session context and location | $\longleftarrow$ | Client Context Vector |
| **2** | Pass 1 (Candidate Retrieval): System retrieves top 200 candidates via Approximate Nearest Neighbor (ANN) vector search | $\longleftarrow$ | 200 Candidate Case Studies |
| **3** | Pass 2 (Business Re-Ranking): System scores each candidate: Score = (Cosine Similarity * 0.35) + (CAS * 0.40) + (GeoRelevance * 0.15) + (Freshness * 0.10) | $\longrightarrow$ | Weighted Rank Matrix |
| **4** | System applies diversity filter to ensure no single creator dominates more than 2 consecutive cards | $\longrightarrow$ | Deduplicated Stream |
| **5** | System returns top 20 ranked case studies to client feed loader | $\longrightarrow$ | Top 20 Ranked Cards |

#### Alternative Courses
**18.1 Cold start: New guest user with zero prior browsing history**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | System detects unauthenticated guest or zero-history profile | $\longleftarrow$ | Cold Start Flag |
| 2a | Pass 1 retrieves platform-wide top trending case studies from Tier 3 Industry Authorities | $\longleftarrow$ | Trending Authority Candidates |
| 3a | Pass 2 optimizes for broad cross-disciplinary diversity (Tech, Legal, Finance) | $\longrightarrow$ | Curated Onboarding Stream |

### Postconditions
1. Feed payload delivered to client app in under 200ms.
2. Ranking weights logged for ML model performance evaluation.

### Exceptions
**E1: Vector store response latency exceeds 150ms timeout**
1. Circuit breaker trips immediately.
2. System serves pre-ranked fallback cache from Redis in <20ms.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Client session vector & location | Client App Request | Ranked Feed Payload (Top 20 items) | Client App |
| Case study embeddings & CAS weights | Vector Store & Redis Cache | Ranking Telemetry Logs | ML Pipeline |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-018 (Two-Pass Recommendation Architecture), FR-001 (Feed Delivery)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-18-01: Verify Pass 2 re-ranking boosts Tier 3 author content ahead of higher cosine match with Tier 1 author.`
- **Boundary & Alternative Test Cases:**
  - `TC-18-02: Test feed diversity filter guarantees no single author has >2 cards in top 10.`
- **Negative & Exception Test Cases:**
  - `TC-18-03: Verify circuit breaker fallback delivers cached feed in < 30ms during vector DB crash.`
