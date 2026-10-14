# Use Case Specification: Fund Milestone Escrow Contract
**Use Case Name:** Fund Milestone Escrow Contract | **ID:** `UC-13` | **Priority:** High

**Actor:** Client / Enterprise Buyer
**Description:** The Client locks project capital into the platform's multi-stage escrow vault for a phased B2B consulting engagement. Funds are held in trust according to a formal Statement of Work (SOW) with defined milestone release conditions.
**Trigger:** Client reviews and accepts a consultant's project proposal / SOW.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Formal SOW proposal created with at least one milestone and agreed deliverables.
2. Both Client and Consultant have agreed to platform Escrow Terms.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Fund and lock milestone escrow contract |  | Escrow Funding |
| **1** | Client reviews proposal: [Milestones 1..N, Due Dates, Deliverables, Acceptance Criteria, Amounts] | $\longleftarrow$ | SOW Proposal Data |
| **2** | Client chooses to fund either Milestone 1 or Full Contract up front | $\longleftarrow$ | Funding Scope selection |
| **3** | Client selects payment rail (M-Pesa, Card, Bank Wire / RTGS for >KES 500,000) | $\longleftarrow$ | Selected Payment Method |
| **4** | System processes transaction through selected gateway | $\longrightarrow$ | Payment Gateway Payload |
| **5** | System confirms receipt and registers funds in immutable Escrow Ledger under contract UUID | $\longrightarrow$ | Escrow Ledger Record |
| **6** | System emits contract state event: 'ESCROW_FUNDED_ACTIVE' | $\longrightarrow$ | Contract State Event |
| **7** | System notifies Consultant that project is funded and authorized to begin work | $\longrightarrow$ | Work Authorization Notice |

#### Alternative Courses
**13.1 Corporate Client pays via Bank Transfer / RTGS invoice**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Client selects 'Bank Wire / RTGS Invoice' option | $\longleftarrow$ | RTGS selection |
| 2a | System issues pro-forma invoice with unique Virtual Account Number (VAN) and reference code | $\longrightarrow$ | Pro-Forma Invoice with VAN |
| 3a | System awaits automated commercial bank reconciliation webhook | $\longleftarrow$ | Bank settlement confirmation |
| 4a | System locks escrow upon settlement confirmation and notifies parties | $\longrightarrow$ | Funded notification |

### Postconditions
1. Escrow contract active with funds securely segregated in partner trust bank.
2. Consultant protected against client default before commencing work.

### Exceptions
**E1: Bank transfer amount mismatch (e.g. less than milestone sum due to wire fees)**
1. System flags underpayment in escrow ledger.
2. System generates balance top-up request to client before milestone activation.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Proposal acceptance & Payment details | Client Input | Escrow Ledger Entry | Platform Financial Ledger |
| Bank / Gateway settlement notifications | Fintech Rails | Work Authorization Notice | Consultant Dashboard |
|  |  | Tax Pro-Forma Invoice | Client Organization |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-013 (Milestone Escrow Architecture), FR-010 (M-Pesa STK Push), FR-011 (Card Rails)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-13-01: Verify successful funding transitions milestone status from DRAFT to FUNDED.`
- **Boundary & Alternative Test Cases:**
  - `TC-13-02: Test high-value escrow contract (KES 2,000,000) funded via multi-tranche RTGS.`
- **Negative & Exception Test Cases:**
  - `TC-13-03: Verify funds remain strictly untouched and unreleased until explicit approval or adjudication.`
