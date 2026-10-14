# Use Case Specification: Initiate Escrow Dispute & Mediation
**Use Case Name:** Initiate Escrow Dispute & Mediation | **ID:** `UC-16` | **Priority:** Medium

**Actor:** Client or Consultant
**Description:** Either party freezes automated escrow releases when an unresolvable breach of contract, non-delivery, or scope disagreement occurs. The dispute locks remaining escrow funds in vault and summons a Platform Escrow Mediator for formal adjudication.
**Trigger:** User clicks 'Raise Dispute & Request Mediation' within milestone dashboard.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Milestone is in 'SUBMITTED_UNDER_REVIEW' or 'REVISIONS_REQUESTED'.
2. At least one round of mutual revision feedback was attempted.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Freeze escrow and file dispute claim |  | Dispute Filing |
| **1** | Aggrieved party clicks 'Raise Dispute' | $\longleftarrow$ | Dispute Initiation |
| **2** | System immediately halts auto-approval countdown and locks milestone escrow funds | $\longrightarrow$ | Escrow Freeze Lock |
| **3** | User selects dispute reason (Non-performance, Specification deviation, Abandonment, Unreasonable revisions) | $\longleftarrow$ | Dispute Category |
| **4** | User uploads supporting evidence (chat logs, SOW clauses, diff files) | $\longleftarrow$ | Evidence dossier |
| **5** | System notifies counter-party and provides 48 hours to submit rebuttal evidence | $\longrightarrow$ | Rebuttal Window Notice |
| **6** | System assigns dispute case ID and routes dossier to Escrow Mediator queue (triggers UC-21) | $\longrightarrow$ | Mediator Case Assignment |

#### Alternative Courses
**16.1 Parties reach mutual amicable settlement before mediator verdict**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Parties negotiate direct compromise (e.g. 50/50 split of milestone) | $\longleftarrow$ | Mutual Settlement Agreement |
| 2a | Both parties sign agreement digitally in dispute portal | $\longleftarrow$ | Digital Signatures |
| 3a | System executes agreed split, unfreezes escrow, and closes dispute case | $\longrightarrow$ | Mutual Settlement Payout |

### Postconditions
1. Escrow funds secured against automatic liquidation.
2. Formal legal dispute case established with immutable evidence timestamps.

### Exceptions
**E1: Counter-party fails to submit rebuttal within 48 hours**
1. Rebuttal timer expires.
2. Case forwarded to mediator with default adverse inference note against non-responding party.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Dispute grounds & evidence files | Initiating Party | Escrow Freeze Command | Escrow Ledger |
| Contract SOW terms & Milestone history | Platform Database | Dispute Case Dossier | Mediator Portal |
|  |  | Legal Notification | Both Contract Parties |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-016 (Escrow Dispute Mediation), FR-021 (Mediator Adjudication)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-16-01: Verify dispute trigger instantly pauses the 72-hour auto-approval clock.`
- **Boundary & Alternative Test Cases:**
  - `TC-16-02: Test simultaneous dispute filing from both parties for the same milestone.`
- **Negative & Exception Test Cases:**
  - `TC-16-03: Verify locked escrow cannot be withdrawn by either party while dispute is OPEN.`
