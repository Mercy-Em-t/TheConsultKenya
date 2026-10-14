# Use Case Specification: Tag Evidence & Proof of Execution
**Use Case Name:** Tag Evidence & Proof of Execution | **ID:** `UC-06` | **Priority:** High

**Actor:** Consultant / Specialist Creator
**Description:** The Consultant links concrete, verifiable evidence to the case study (such as GitHub/GitLab repository commit tags, live production URLs, anonymized client contracts, or audit documents) to substantiate claimed outcomes.
**Trigger:** Consultant navigates to the 'Evidence & Verification' tab in the Creation Studio.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Case study draft is created.
2. External accounts (e.g. GitHub) connected if repository proof is used.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Attach verifiable evidence and execution proofs |  | Evidence Attachment |
| **1** | Consultant selects evidence type (GitHub Commit Link, Live Domain URL, PDF Audit Memo, Client Co-Sign) | $\longleftarrow$ | Evidence Type |
| **2** | Consultant provides proof URL or uploads sanitized document | $\longleftarrow$ | Proof URL / Uploaded Asset |
| **3** | System queries external API (e.g., GitHub API to verify commit hash, author, and timestamp) | $\longleftarrow$ | External Proof API response |
| **4** | System generates cryptographic SHA-256 hash of the evidence snapshot | $\longrightarrow$ | Evidence SHA-256 Digest |
| **5** | System badges the evidence item as 'Verified Execution Proof' | $\longrightarrow$ | Verified Evidence Badge |
| **6** | Consultant links specific claims in the case study text to the attached proof badges | $\longleftarrow$ | Claim-to-Proof link mapping |

#### Alternative Courses
**6.1 Client Co-Sign verification request**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Consultant enters verified corporate client email address for co-attestation | $\longleftarrow$ | Client corporate email |
| 2a | System dispatches magic verification token to client stakeholder | $\longrightarrow$ | Client attestation token |
| 3a | Evidence displays 'Pending Client Attestation' until authenticated signature received | $\longrightarrow$ | Pending badge state |

### Postconditions
1. Evidence records linked to the case study entity with immutable timestamps.
2. Creator Authority Score potential boosts calculated for publication.

### Exceptions
**E1: Invalid or broken external URL / 404 commit link**
1. System displays validation error: 'Unable to reach repository commit. Please verify repository is public or authorize private read access.'
2. System rejects evidence submission until resolved.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Proof URLs, GitHub credentials, PDF files | Consultant Input | Cryptographic Evidence Record | Evidence Vault Datastore |
| GitHub / GitLab API verification response | External Repository Rails | Verified Proof Badges | Case Study View |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-006 (Evidence Verification & Attestation), FR-017 (CAS Credibility Metrics)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-06-01: Verify GitHub commit hash query confirms author match and displays commit date.`
- **Boundary & Alternative Test Cases:**
  - `TC-06-02: Test upload of 25MB encrypted PDF audit memo with automatic metadata stripping.`
- **Negative & Exception Test Cases:**
  - `TC-06-03: Verify handling of rate-limited external APIs with exponential backoff.`
