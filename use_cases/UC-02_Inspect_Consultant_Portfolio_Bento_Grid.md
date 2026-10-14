# Use Case Specification: Inspect Consultant Portfolio (Bento Grid)
**Use Case Name:** Inspect Consultant Portfolio (Bento Grid) | **ID:** `UC-02` | **Priority:** High

**Actor:** Client / Enterprise Buyer
**Description:** The Client views a consultant's public authority profile presented as a high-density, modular Bento grid. The profile displays verified professional credentials, live booking rates, featured visual case studies, execution proofs, and client reviews.
**Trigger:** Client clicks on a consultant's avatar, handle, or author badge from a case study or search result.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Consultant profile exists and has completed minimum profile onboarding.
2. Consultant public visibility is set to active.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | View consultant authority Bento portfolio |  | Profile Request |
| **1** | Client requests consultant profile by handle or ID | $\longleftarrow$ | Consultant Handle / ID |
| **2** | System retrieves verified credentials, CAS score, bio, and Bento grid modules | $\longleftarrow$ | Consultant Profile Datastore |
| **3** | System retrieves active booking packages, availability calendar, and escrow history | $\longleftarrow$ | Booking & Escrow DB |
| **4** | System renders Bento Grid: [Bio & Tier Badge | Featured Case Studies | Booking Widget | Verification Seals | Client Proofs] | $\longrightarrow$ | Modular Bento Grid UI |
| **5** | Client inspects verified credential seals (e.g. LSK, ICPAK, EBK, GitHub) | $\longleftarrow$ | Badge inspection tap |
| **6** | System presents cryptographic validation modal verifying external registry confirmation | $\longrightarrow$ | Registry verification modal |
| **7** | Client reviews consultant past project ratings and escrow completion rate | $\longrightarrow$ | Escrow completion statistics |

#### Alternative Courses
**2.1 Consultant has zero published case studies (brand new onboarded creator)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | System detects empty case study portfolio | $\longleftarrow$ | Empty deck flag |
| 2a | System renders Bento layout highlighting verified identity, academic qualifications, and intro advisory call offer | $\longrightarrow$ | Starter Bento template |

### Postconditions
1. Profile view counter incremented for consultant analytics.
2. Client recently-viewed consultant stack updated.

### Exceptions
**E1: Consultant profile is suspended or under moderation review**
1. System displays notice: 'This consultant profile is currently under review.'
2. System restricts booking button and redirects user to topic search.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Consultant Handle / ID | Client Navigation | Bento Grid Profile Layout | Client UI |
| Credential & Verification records | Identity Verification Datastore | Cryptographic Registry Proof | Verification Modal UI |
| Consultant engagement metrics | CAS Telemetry Database |  |  |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-002 (Bento Profile Architecture), FR-008 (Credential Verification Display), FR-009 (Booking Anchor Integration)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-02-01: Verify Bento grid renders all 6 modules within 500ms.`
  - `TC-02-02: Verify verification seals open valid modal with registry timestamp.`
- **Boundary & Alternative Test Cases:**
  - `TC-02-03: Verify layout responsiveness on both 360px mobile screen and 4K ultra-wide monitor.`
- **Negative & Exception Test Cases:**
  - `TC-02-04: Verify suspended profile hides booking triggers and displays compliant notice.`
