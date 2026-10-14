# Use Case Specification: Review & Approve Escrow Milestone
**Use Case Name:** Review & Approve Escrow Milestone | **ID:** `UC-15` | **Priority:** High

**Actor:** Client / Enterprise Buyer
**Description:** The Client reviews the consultant's submitted deliverable. Upon satisfaction, the client clicks 'Approve & Release Funds'. The system automatically calculates platform take rate (5-8%), generates a KRA eTIMS tax invoice, releases net payout to the consultant via M-Pesa B2C or bank transfer, and updates project status.
**Trigger:** Client reviews deliverable and clicks 'Approve Milestone'.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Milestone status is 'SUBMITTED_UNDER_REVIEW'.
2. Funds are currently locked in escrow.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Approve deliverable and disburse escrow payout |  | Milestone Approval |
| **1** | Client accesses deliverable review dashboard and verifies submitted deliverables against SOW criteria | $\longleftarrow$ | Inspection Action |
| **2** | Client clicks 'Approve Milestone & Release Funds' | $\longleftarrow$ | Approval Command |
| **3** | System displays release confirmation modal with breakdown: [Milestone Total | Platform Commission (7%) | Withholding Tax | Net Consultant Payout] | $\longrightarrow$ | Fee Breakdown Modal |
| **4** | Client enters 2FA code / biometric confirmation | $\longleftarrow$ | Client 2FA Token |
| **5** | System executes financial settlement in double-entry ledger | $\longrightarrow$ | Ledger Settlement Record |
| **6** | System transmits electronic invoice to KRA eTIMS API and attaches official QR code | $\longrightarrow$ | KRA eTIMS Invoice Submission |
| **7** | System triggers automated B2C payout to consultant via M-Pesa B2C or RTGS | $\longrightarrow$ | B2C Payout Instruction |
| **8** | Consultant receives instant payout notification and funds in mobile wallet | $\longrightarrow$ | Payout Notification |
| **9** | System transitions milestone status to 'COMPLETED_RELEASED' | $\longrightarrow$ | Milestone State Update |

#### Alternative Courses
**15.1 72-hour review timer elapses without client action (Auto-Approval)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | 72-hour inspection countdown reaches 0 with no client dispute or rejection filed | $\longleftarrow$ | Timer Expiry Trigger |
| 2a | System automatically invokes step 5 through step 9 of Normal Course under contractual auto-approval policy | $\longrightarrow$ | Auto-Approval Execution |
| 3a | System sends notification to client: 'Milestone auto-approved per platform terms.' | $\longrightarrow$ | Auto-Approval notice |

**15.2 Client requests revisions (branch at step 2)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Client clicks 'Request Revisions' and inputs specific unfulfilled requirements | $\longleftarrow$ | Revision Feedback Notes |
| 2a | Milestone status transitions to 'REVISIONS_REQUESTED' | $\longrightarrow$ | Revision Status |
| 3a | Consultant notified to submit updated deliverable (UC-14) | $\longrightarrow$ | Revision Task Notice |

### Postconditions
1. Net funds disbursed to consultant.
2. Platform commission credited to KenyaConsult operational account.
3. KRA eTIMS tax invoice generated with cryptographic QR code.
4. Consultant's CAS score updated with successful milestone completion points.

### Exceptions
**E1: B2C M-Pesa payout API failure (e.g. utility wallet underfunded or telco timeout)**
1. System flags payout as 'PENDING_MANUAL_DISBURSEMENT' without losing ledger state.
2. Finance team alerted via PagerDuty to replenish corporate B2C account.
3. Automated retry worker executes payout within 30 minutes.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Client approval confirmation & 2FA token | Client Input | B2C Mobile Payout / Bank Wire | Consultant Mobile Wallet |
| Milestone contract financial parameters | Escrow Ledger | KRA eTIMS Electronic Invoice | KRA Tax Registry & Client |
|  |  | Completed Ledger Entry | Platform Financial Ledger |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-015 (Escrow Release Engine), FR-016 (Dispute Handling), FR-022 (Tax & eTIMS Compliance)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-15-01: Verify fund release accurately applies 7% commission and credits net balance.`
- **Boundary & Alternative Test Cases:**
  - `TC-15-02: Test automatic auto-approval execution at exactly 72 hours 00 minutes 01 seconds.`
- **Negative & Exception Test Cases:**
  - `TC-15-03: Verify transaction rollback if ledger database fails during settlement step.`
