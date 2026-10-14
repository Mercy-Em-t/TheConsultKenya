# Use Case Specification: Manage Phased Rollout & Creator Onboarding
**Use Case Name:** Manage Phased Rollout & Creator Onboarding | **ID:** `UC-19` | **Priority:** Medium

**Actor:** Platform Administrator
**Description:** The Administrator manages the controlled phased rollout of Consult Kenya. The workflow governs transitions across Phase 1 (Anchor Agency Onboarding), Phase 2 (Curated Beta with invite codes), and Phase 3 (Open Ecosystem with automated verification).
**Trigger:** Admin updates rollout parameters in Admin Console.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Admin is authenticated with superuser MFA permissions.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Configure platform rollout phase and creator quotas |  | Rollout Governance |
| **1** | Admin accesses Rollout Governance dashboard | $\longleftarrow$ | Admin Access |
| **2** | Admin views current cohort statistics: [Active Creators, Pending Invites, Verification Backlog, Take Rate] | $\longrightarrow$ | Cohort Metrics |
| **3** | Admin generates batch of 50 VIP Invite Codes for curated pilot consultants | $\longleftarrow$ | Invite Code Generation Command |
| **4** | System produces cryptographically signed, one-time invite tokens | $\longrightarrow$ | Invite Tokens |
| **5** | Admin configures platform take rate (e.g., set to introductory 5% for Phase 1 partners) | $\longleftarrow$ | Take rate configuration |
| **6** | System updates billing engine parameters across all new contract initializations | $\longrightarrow$ | Updated Billing Config |

#### Alternative Courses
**19.1 Admin triggers rollout transition to Phase 3 (Open Ecosystem)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Admin selects 'Activate Open Ecosystem' | $\longleftarrow$ | Open Phase Command |
| 2a | System removes invite code requirement and enables automated registry self-onboarding | $\longrightarrow$ | Public Onboarding Enabled |

### Postconditions
1. Updated rollout policy enforced platform-wide.
2. Admin action logged in security audit vault.

### Exceptions
**E1: Unauthorized attempt to modify platform take rate without secondary approval**
1. System requires second admin multi-signature sign-off for financial parameter changes.
2. Change remains pending until second admin approves.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Rollout phase toggle, invite batches, commission rates | Platform Administrator | Cryptographic Invite Codes | Admin Dashboard |
|  |  | Updated Platform Operational Parameters | System Configuration DB |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-019 (Phased Rollout Management), FR-020 (Admin Governance)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-19-01: Verify valid invite code grants creator onboarding access during Phase 2 Curated Beta.`
- **Boundary & Alternative Test Cases:**
  - `TC-19-02: Test invite code exhaustion after single use.`
- **Negative & Exception Test Cases:**
  - `TC-19-03: Verify take rate modification requires dual admin approval.`
