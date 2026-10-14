# Use Case Specification: Conduct Secure Live Consultation
**Use Case Name:** Conduct Secure Live Consultation | **ID:** `UC-12` | **Priority:** High

**Actor:** Client & Consultant
**Description:** At the scheduled time, the Client and Consultant join an encrypted, zero-friction in-browser WebRTC video consultation room. The room provides screen sharing, collaborative note-taking, and automatically logs session duration and completion.
**Trigger:** Scheduled appointment time arrives or either party clicks 'Join Consultation Room'.
**Type:** [x] External  [x] Temporal

### Preconditions
1. Booking status is 'CONFIRMED_ESCROW_LOCKED'.
2. Both parties have verified access tokens.
3. Client and consultant devices support WebRTC.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Conduct live video consultation and record session artifacts |  | Live Consultation |
| **1** | Client and Consultant access meeting URL within 10 minutes of scheduled start | $\longleftarrow$ | Room Access Token |
| **2** | System verifies meeting validity, checks participant credentials, and opens WebRTC media room | $\longrightarrow$ | Encrypted WebRTC Channel |
| **3** | Both participants join with mutual audio/video streams established | $\longrightarrow$ | Live A/V Streams |
| **4** | Participants collaborate using in-app screen sharing and shared action item scratchpad | $\longleftarrow$ | Collaborative Notes & Action Items |
| **5** | System records real-time call telemetry (start timestamp, end timestamp, connection quality) | $\longrightarrow$ | Call Telemetry Record |
| **6** | Session concludes; either participant clicks 'End Session' | $\longleftarrow$ | Session End Command |
| **7** | System compiles meeting action summary and sends copy to both parties | $\longrightarrow$ | Meeting Summary & Action Items |
| **8** | System transitions booking to 'SESSION_COMPLETED_PENDING_REVIEW' | $\longrightarrow$ | Updated Booking Entity |

#### Alternative Courses
**12.1 Either party experiences connection drop during call (network reconnection)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | WebRTC peer connection drops due to unstable internet | $\longleftarrow$ | Connection Drop event |
| 2a | System maintains room open for 15-minute grace period and displays reconnection banner | $\longrightarrow$ | Reconnection Waiting Room |
| 3a | Disconnected party rejoins and session resumes | $\longleftarrow$ | Reconnection token |

**12.2 Consultant or Client is a no-show (15 minutes elapsed)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | System timer reaches 15 minutes past start with only one party present | $\longleftarrow$ | No-Show timer trigger |
| 2a | System logs verified no-show timestamp | $\longrightarrow$ | No-Show Event Record |
| 3a | If Consultant no-show: Full refund initiated to Client. If Client no-show: 50% cancellation fee paid to Consultant. | $\longrightarrow$ | Escrow Policy Action |

### Postconditions
1. Meeting completion timestamp permanently logged.
2. Both parties prompted for private session feedback and ratings.
3. Escrow release window initiates.

### Exceptions
**E1: Browser denies camera or microphone permissions**
1. System displays modal with illustrated browser permission fix steps.
2. System provides one-click option to switch to audio-only mode.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Meeting room access tokens, audio/video streams | Browser WebRTC API | Encrypted WebRTC Audio/Video Session | Participant Browsers |
| In-session notes and screen share events | Participants | Action Items & Meeting Summary PDF | Client & Consultant Email |
|  |  | Session Completion Telemetry | Escrow Ledger |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-012 (WebRTC Video Infrastructure), FR-015 (Escrow Release Engine)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-12-01: Verify peer-to-peer connection establishes under 2 seconds on standard fiber/4G.`
- **Boundary & Alternative Test Cases:**
  - `TC-12-02: Test automated no-show policy triggering at exactly 15 minutes 00 seconds.`
- **Negative & Exception Test Cases:**
  - `TC-12-03: Verify end-to-end media encryption (DTLS-SRTP) prevents unauthorized eavesdropping.`
