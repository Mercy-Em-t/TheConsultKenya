# Use Case Specification: Adjudicate Milestone Dispute
**Use Case Name:** Adjudicate Milestone Dispute | **ID:** `UC-21` | **Priority:** Medium

**Actor:** Escrow Mediator / Legal Counsel
**Description:** An appointed Escrow Mediator evaluates evidence submitted by both Client and Consultant in a disputed milestone, interprets contractual SOW acceptance criteria, and issues a legally binding apportionment and fund disbursement ruling.
**Trigger:** Mediator opens pending case from Escrow Dispute Queue (following UC-16).
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Dispute case opened with both claimant dossier and respondent rebuttal.
2. Milestone funds frozen in escrow vault.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Adjudicate milestone dispute and disburse escrow |  | Dispute Adjudication |
| **1** | Mediator reviews SOW deliverables, GitHub commits, milestone artifacts, and chat transcripts | $\longleftarrow$ | Case Evidence Dossier |
| **2** | Mediator conducts independent technical or domain verification (e.g. audits if code compiles or tax memo meets standards) | $\longleftarrow$ | Independent audit findings |
| **3** | Mediator enters adjudication decision: [Full Release to Consultant | Full Refund to Client | Prorated Settlement (e.g. 60% Consultant, 40% Client)] | $\longleftarrow$ | Adjudication Verdict |
| **4** | Mediator inputs written justification rationale citing contract clause numbers | $\longleftarrow$ | Legal Ruling Rationale |
| **5** | System prompts Mediator for biometric / hardware token approval | $\longleftarrow$ | Mediator Security Token |
| **6** | System executes binding fund disbursement from escrow according to verdict | $\longrightarrow$ | Disbursement Execution |
| **7** | System issues formal Adjudication Certificate PDF to both parties and closes dispute case | $\longrightarrow$ | Adjudication Certificate PDF |

#### Alternative Courses
**21.1 Mediator requests additional clarifying documentation from parties**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Mediator issues formal request for supplemental evidence with 24-hour deadline | $\longrightarrow$ | Request for Evidence |
| 2a | Parties upload requested files; mediator resumes review at step 2 | $\longleftarrow$ | Supplemental files |

### Postconditions
1. Frozen escrow funds liquidated and disbursed to determined parties.
2. Dispute marked 'CLOSED_RESOLVED'.
3. Permanent record logged in legal archive.

### Exceptions
**E1: System detects potential conflict of interest between mediator and participant**
1. Algorithm flags shared prior engagements.
2. Case automatically reassigned to alternate neutral mediator.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Dispute case evidence, SOW, Deliverables | Dispute Vault | Escrow Disbursement Commands | Platform Payment Rails |
| Mediator verdict & legal rationale | Escrow Mediator | Adjudication Certificate PDF | Client & Consultant |
|  |  | Immutable Legal Audit Log | Platform Regulatory Vault |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-021 (Escrow Dispute Adjudication), FR-016 (Dispute Intake)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-21-01: Verify prorated ruling (e.g., 70/30) executes exact currency math without fractional cent loss.`
- **Boundary & Alternative Test Cases:**
  - `TC-21-02: Test mediator ruling on zero-balance or expired authorization.`
- **Negative & Exception Test Cases:**
  - `TC-21-03: Verify mediator verdict cannot be altered once digitally signed.`
