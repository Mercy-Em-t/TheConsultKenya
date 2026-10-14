# Use Case Specification: Attach Conversion Anchor Call-to-Action
**Use Case Name:** Attach Conversion Anchor Call-to-Action | **ID:** `UC-07` | **Priority:** High

**Actor:** Consultant / Specialist Creator
**Description:** The Consultant configures a native conversion anchor at the bottom of the case study. This hook enables readers to immediately take commercial action (e.g., 'Book 30-Min Strategy Call - KES 10,000', 'Request Architecture Audit SOW', or 'Hire via Milestone Escrow').
**Trigger:** Consultant completes case study content and navigates to the 'Conversion Hook' step.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Consultant has configured billing rates or calendar availability.
2. Case study content meets publication minimums.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Configure native business conversion anchor |  | Anchor Setup |
| **1** | Consultant selects conversion anchor type (Live Advisory Session, Fixed-Price Audit, SOW Proposal Inquiry) | $\longleftarrow$ | Anchor Type |
| **2** | Consultant defines price in KES / USD and service duration (e.g., KES 15,000 for 45 mins) | $\longleftarrow$ | Pricing & Duration parameters |
| **3** | Consultant specifies intake form questionnaire required from client before booking | $\longleftarrow$ | Intake questionnaire fields |
| **4** | System validates pricing complies with platform minimums and Kenyan tax rules | $\longrightarrow$ | Pricing validation status |
| **5** | System embeds sticky conversion drawer at base of case study deck | $\longrightarrow$ | Configured Conversion Anchor |

#### Alternative Courses
**7.1 Consultant links anchor to custom Enterprise RFP inquiry**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Consultant selects 'Custom SOW Inquiry' without fixed pricing | $\longleftarrow$ | RFP option flag |
| 2a | System configures RFP submission wizard with NDA checkbox and budget bracket dropdown | $\longrightarrow$ | RFP Wizard setup |

### Postconditions
1. Case study is equipped with actionable commercial trigger ready for publishing.
2. Anchor configuration stored in case study metadata.

### Exceptions
**E1: Pricing below statutory or platform minimum**
1. System displays warning: 'Advisory consultation price cannot be lower than KES 2,500.'
2. Consultant adjusts price to continue.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Anchor type, fee amount, intake questions | Consultant Input | Conversion Anchor Configuration | Case Study Datastore |
|  |  | Rendered Sticky CTA Drawer | Reader Interface |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-007 (Conversion Anchor Infrastructure), FR-009 (Consultation Scheduling)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-07-01: Verify conversion CTA persists and renders correctly across mobile viewport.`
- **Boundary & Alternative Test Cases:**
  - `TC-07-02: Verify multi-currency price conversion (KES to USD/EUR) based on daily CBK rates.`
- **Negative & Exception Test Cases:**
  - `TC-07-03: Verify attempt to publish without active calendar fails with helpful guidance.`
