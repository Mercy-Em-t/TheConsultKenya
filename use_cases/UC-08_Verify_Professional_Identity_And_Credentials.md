# Use Case Specification: Verify Professional Identity & Credentials
**Use Case Name:** Verify Professional Identity & Credentials | **ID:** `UC-08` | **Priority:** High

**Actor:** Consultant / Specialist Creator
**Description:** The Consultant submits national identification documents and regulatory professional licenses (e.g., Law Society of Kenya - LSK, ICPAK, Engineers Board of Kenya - EBK) for formal verification against statutory registries to earn verified platform authority tiers.
**Trigger:** Consultant initiates verification in the 'Trust & Authority' section of settings.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Consultant is logged into KenyaConsult.
2. Government and professional API gateways (IPRS/eCitizen, LSK, ICPAK, EBK) are reachable or queueable.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Verify identity and professional board credentials |  | Verification Initiation |
| **1** | Consultant selects verification category (National ID / Passport, Professional Body License, Tax PIN) | $\longleftarrow$ | Verification Category |
| **2** | Consultant enters National ID Number, KRA PIN, and Professional Practicing Certificate Number | $\longleftarrow$ | ID & Registration Credentials |
| **3** | Consultant uploads scan of Practicing Certificate and national document | $\longleftarrow$ | Scanned Document files |
| **4** | System queries government IPRS / KRA API to validate ID and tax compliance status | $\longleftarrow$ | IPRS / KRA API validation response |
| **5** | System queries professional board registry (e.g. LSK Advocate Roll, ICPAK Member Register) | $\longleftarrow$ | Board Registry verification data |
| **6** | System confirms match of full name, registration number, and active standing | $\longrightarrow$ | Match Confirmation status |
| **7** | System awards 'Verified Specialist' badge and upgrades CAS tier from Tier 1 to Tier 3 | $\longrightarrow$ | Awarded Badge & CAS multiplier |
| **8** | System logs cryptographic verification timestamp in the immutable audit ledger | $\longrightarrow$ | Audit Ledger entry |

#### Alternative Courses
**8.1 Automated registry API is offline or requires manual review (branch at step 5)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | System detects board registry timeout or manual verification requirement | $\longleftarrow$ | Registry API timeout |
| 2a | System queues application into Compliance Officer review queue (UC-20) | $\longrightarrow$ | Manual Review Queue entry |
| 3a | System notifies consultant: 'Credentials submitted. Manual review completes within 24 hours.' | $\longrightarrow$ | Pending review notice |

### Postconditions
1. Consultant profile displays verified credentials seals.
2. Consultant CAS score increased by 40% authoritative weighting.
3. Sensitive documents securely encrypted with AES-256 and PII redacted from public views.

### Exceptions
**E1: Name mismatch between National ID and Professional Board License (occurs at step 6)**
1. System flags discrepancy: 'Name on LSK License does not match National ID. Please upload official deed poll or contact support.'
2. Application flagged for manual verification officer.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| National ID, KRA PIN, Board Registration #, Certificate Scans | Consultant Input | Verified Authority Badges | Consultant Profile UI |
| Registry API verification payloads | IPRS / KRA / LSK / ICPAK / EBK APIs | Upgraded CAS Multiplier | Recommendation Engine |
|  |  | Verification Audit Record | Compliance Vault |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-008 (Identity & Credential Verification), FR-017 (CAS Tiering), FR-020 (Compliance & Moderation)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-08-01: Verify valid ICPAK practicing member number updates profile badge in < 5 seconds.`
- **Boundary & Alternative Test Cases:**
  - `TC-08-02: Test high-resolution PDF upload (15MB) with automatic EXIF/PII sanitization.`
- **Negative & Exception Test Cases:**
  - `TC-08-03: Verify expired practicing certificate triggers alert and rejects tier upgrade.`
