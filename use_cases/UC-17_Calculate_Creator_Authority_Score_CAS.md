# Use Case Specification: Calculate Creator Authority Score (CAS)
**Use Case Name:** Calculate Creator Authority Score (CAS) | **ID:** `UC-17` | **Priority:** High

**Actor:** Automated System Daemon
**Description:** The background intelligence daemon continuously computes the multi-factor Creator Authority Score (CAS) for each specialist. CAS combines credential verification level, peer attestations, completed escrow track record, client reviews, and content dwell telemetry to determine organic reach and badge tiers.
**Trigger:** Temporal trigger: Runs hourly batch cycle, and immediately upon major events (milestone completed, credential verified).
**Type:** [ ] External  [x] Temporal

### Preconditions
1. Creator has published profile or active content.
2. Telemetry and verification datastores are online.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Compute multi-factor Creator Authority Score |  | CAS Computation |
| **1** | System daemon gathers creator input vectors: [Registry Verification Tier (40%), Completed Escrow Contracts (30%), Case Study Saves & Dwell (20%), Peer Attestations (10%)] | $\longleftarrow$ | Creator Vector Telemetry |
| **2** | System applies anti-gaming heuristic (detects circular reviews, self-booking, bot dwell) | $\longleftarrow$ | Anomaly Detection Weights |
| **3** | System calculates normalized CAS score on a scale of 0 to 1,000 points | $\longrightarrow$ | Computed CAS Float |
| **4** | System updates Creator Authority Tier: [Tier 1: Emerging Creator (0-399) | Tier 2: Established Practitioner (400-699) | Tier 3: Industry Authority (700-1,000)] | $\longrightarrow$ | Updated Tier Classification |
| **5** | System writes updated CAS weights into Redis cache for high-speed feed ranking (UC-18) | $\longrightarrow$ | Redis CAS Cache Record |

#### Alternative Courses
**17.1 Anomaly detected (Sybil attack or artificial metric inflation)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Anti-gaming engine detects suspicious clustered IP views or circular payments | $\longleftarrow$ | Fraud Anomaly Flag |
| 2a | System dampens score gain and flags profile for Trust & Safety review (UC-20) | $\longrightarrow$ | Trust & Safety Alert |

### Postconditions
1. Creator CAS updated across all platform services.
2. Feed recommendation weights adjusted.

### Exceptions
**E1: Missing telemetry partitions during calculation**
1. Daemon utilizes last known valid CAS score.
2. Error logged to system monitoring; calculation rescheduled in 15 minutes.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Registry data, completed milestone records, dwell telemetry | Platform Datastores | Updated CAS Score & Authority Tier | Creator Profile & Redis Cache |
|  |  | Feed Ranking Multiplier | Discovery Recommendation Pipeline |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-017 (Creator Authority Scoring Engine), FR-018 (Algorithmic Ranking)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-17-01: Verify adding verified LSK license increases CAS by precisely calculated 40% weight.`
- **Boundary & Alternative Test Cases:**
  - `TC-17-02: Test CAS calculation across 100,000 active creators within 60-second batch window.`
- **Negative & Exception Test Cases:**
  - `TC-17-03: Verify circular booking ring is flagged and receives zero CAS boost.`
