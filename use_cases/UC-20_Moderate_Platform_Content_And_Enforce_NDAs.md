# Use Case Specification: Moderate Platform Content & Enforce NDAs
**Use Case Name:** Moderate Platform Content & Enforce NDAs | **ID:** `UC-20` | **Priority:** High

**Actor:** Platform Administrator / Compliance Officer
**Description:** The Administrator and automated moderation daemons review flagged case studies, prevent enterprise non-disclosure agreement (NDA) leaks, detect spam, and redact unauthorized proprietary client information.
**Trigger:** External: User flags a case study; Automated: Content ingestion scanner detects potential client confidential data.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Case study submitted or reported.
2. Automated DLP (Data Loss Prevention) regex scanners active.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Audit flagged content and enforce compliance action |  | Content Moderation |
| **1** | System flags case study containing high-risk tokens (e.g. unredacted bank account numbers, API secrets, confidential client names) | $\longleftarrow$ | DLP Scanner Trigger |
| **2** | System moves case study to 'PENDING_MODERATION' and notifies reviewer | $\longrightarrow$ | Moderation Queue Item |
| **3** | Compliance Officer inspects highlighted sensitive text snippets in split-screen diff tool | $\longleftarrow$ | Audit View |
| **4** | Officer applies automated Redactor tool to blur sensitive figures while preserving educational architecture | $\longleftarrow$ | Redaction Command |
| **5** | Officer approves sanitized version and publishes deck | $\longrightarrow$ | Sanitized Case Study |
| **6** | System sends compliance advisory note to author | $\longrightarrow$ | Author Compliance Note |

#### Alternative Courses
**20.1 Severe violation (plagiarism, willful breach of corporate trade secret, malicious code)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Officer selects 'Take Down & Issue Strike' | $\longleftarrow$ | Take-down Command |
| 2a | System removes deck from public feed immediately, adds strike to author profile, and docks CAS points by 200 | $\longrightarrow$ | Enforcement Action |

### Postconditions
1. Platform remains free from trade secret liability.
2. Comprehensive audit trail recorded.

### Exceptions
**E1: Author files dispute against moderation take-down**
1. Author submits proof of authorization or written client consent.
2. Senior legal counsel reviews and can reinstate post.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Flagged content, reports, scanner detections | System / Users | Sanitized Published Content / Takedown Notice | Public Platform |
| Moderation decisions & redactions | Compliance Officer | Author Infraction Record | Creator Profile Ledger |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-020 (Content Moderation & NDA Redaction), FR-017 (CAS Penalties)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-20-01: Verify DLP scanner flags AWS API keys or KRA PINs in code blocks before publish.`
- **Boundary & Alternative Test Cases:**
  - `TC-20-02: Test automated take-down latency (< 1 second) upon critical trade secret notice.`
- **Negative & Exception Test Cases:**
  - `TC-20-03: Verify docked CAS points properly recalculate creator's rank.`
