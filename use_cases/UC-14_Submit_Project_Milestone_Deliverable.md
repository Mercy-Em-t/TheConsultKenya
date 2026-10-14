# Use Case Specification: Submit Project Milestone Deliverable
**Use Case Name:** Submit Project Milestone Deliverable | **ID:** `UC-14` | **Priority:** High

**Actor:** Consultant / Specialist Creator
**Description:** The Consultant uploads finished project deliverables (code, documents, blueprints, reports) for an active escrow milestone. The system computes a cryptographic SHA-256 fingerprint, timestamps the submission, and triggers the client's 72-hour review window.
**Trigger:** Consultant clicks 'Submit Deliverable' on an active milestone in project dashboard.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Project contract status is 'ESCROW_FUNDED_ACTIVE'.
2. Milestone status is 'IN_PROGRESS'.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Submit milestone deliverable with cryptographic fingerprint |  | Deliverable Submission |
| **1** | Consultant navigates to active milestone and clicks 'Submit Deliverable' | $\longleftarrow$ | Submit Trigger |
| **2** | Consultant provides completion notes, live links (GitHub PR, staging URL), and file uploads | $\longleftarrow$ | Deliverable Files & Links |
| **3** | System uploads files to encrypted cloud storage and generates SHA-256 cryptographic hash of all files | $\longrightarrow$ | SHA-256 Artifact Digests |
| **4** | System stores immutable delivery record with server timestamp | $\longrightarrow$ | Delivery Audit Record |
| **5** | System transitions milestone status to 'SUBMITTED_UNDER_REVIEW' | $\longrightarrow$ | Milestone State Update |
| **6** | System starts 72-hour inspection countdown timer | $\longrightarrow$ | 72-Hour Inspection Timer |
| **7** | System dispatches instant notification and review link to Client | $\longrightarrow$ | Client Review Notification |

#### Alternative Courses
**14.1 Consultant uploads revisions following client feedback**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Consultant submits updated assets addressing requested changes | $\longleftarrow$ | Revised assets |
| 2a | System creates new deliverable revision (v2), resets review countdown, and preserves v1 for dispute audit | $\longrightarrow$ | Revision versioning |

### Postconditions
1. Deliverable assets secured in tamper-proof repository.
2. 72-hour auto-approval clock running.

### Exceptions
**E1: Uploaded deliverable contains infected or prohibited file types (.exe, malware)**
1. Malware scanner isolates uploaded artifact in sandbox.
2. System rejects upload with security alert: 'Prohibited file type detected.'
3. Consultant prompted to upload clean archive.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Deliverable files, PR links, completion summary | Consultant Input | Encrypted Artifacts & SHA-256 Hashes | Cloud Object Storage |
|  |  | 72-Hour Review Timer Event | Task Scheduler / Celery |
|  |  | Client Review Notification | Client Email & In-App |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-014 (Cryptographic Deliverable Proofs), FR-015 (Inspection Window Timer)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-14-01: Verify SHA-256 hash matches exact byte content of uploaded deliverable archive.`
- **Boundary & Alternative Test Cases:**
  - `TC-14-02: Test submission right at the exact milestone deadline (23:59:59).`
- **Negative & Exception Test Cases:**
  - `TC-14-03: Verify virus scanner quarantines test EICAR file without affecting platform stability.`
