# Business Process Specification: Manage User Identity, Onboarding & Professional Verification
**Process ID:** `PROC-1.0` | **Owner:** Consultant / Client / Compliance Officer

### Description
Handles account registration, multi-factor authentication, profile creation, and statutory credential validation against Kenyan government and professional bodies (IPRS, KRA, LSK, ICPAK, EBK).

### Associated External Entities
- **Client**
- **Consultant**
- **Platform Administrator**
- **Government & Professional Registries (IPRS, KRA, LSK, ICPAK, EBK)**

### Associated Data Stores
- **D1: User & Credential Registry**
- **D2: Compliance & Audit Vault**
- **D8: Configuration & Policy Datastore**

### Data Flow Analysis (Inputs & Outputs)
| Flow Direction | Data Flow Name / Payload | Source / Origin | Destination |
| :---: | :--- | :--- | :--- |
| $\longleftarrow$ (Inflow) | Registration details & Credentials | Client / Consultant | `PROC-1.0` |
| $\longleftarrow$ (Inflow) | National ID, KRA PIN, Board Registration # & License scan | Consultant | `PROC-1.0` |
| $\longleftarrow$ (Inflow) | Verification responses & standing status | Registries API | `PROC-1.0` |
| $\longleftarrow$ (Inflow) | Invite Codes & Cohort Policy | Platform Administrator | `PROC-1.0` |
| $\longrightarrow$ (Outflow) | Authentication Tokens & Session Profile | `PROC-1.0` | Client / Consultant |
| $\longrightarrow$ (Outflow) | Verification Query Payload | `PROC-1.0` | Registries API |
| $\longrightarrow$ (Outflow) | Verified Specialist Seal & Authority Tier Upgrade | `PROC-1.0` | Consultant Profile / D1 |
| $\longrightarrow$ (Outflow) | Compliance Audit Log Record | `PROC-1.0` | D2: Compliance & Audit Vault |

### Decomposed Sub-Processes (Level 1 DFD Scope)
| Sub-Process ID | Sub-Process Name | Operational Description |
| :---: | :--- | :--- |
| **1.1** | Register & Authenticate User | Validates user contact info, issues OTP/MFA, and establishes session. |
| **1.2** | Curate Profile & Bento Grid Architecture | Structures bio, skill tags, case study previews, and fee schedules. |
| **1.3** | Ingest & Sanitize Professional Credentials | Extracts metadata from licenses and scrubs PII from public view. |
| **1.4** | Verify Credentials via External Registries | Executes automated checks against IPRS, KRA, and professional board APIs. |
| **1.5** | Manage Cohort Onboarding & Invite Codes | Enforces rollout gates (Anchor Agency -> Curated Beta -> Open Ecosystem). |
