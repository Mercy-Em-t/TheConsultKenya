# Business Process Specification: Manage Milestone SOW Contracts, Deliverables & Payouts
**Process ID:** `PROC-6.0` | **Owner:** Client / Consultant / KRA eTIMS / B2C Payout Rail

### Description
Governs multi-stage SOW consulting contracts, cryptographic delivery fingerprinting, 72-hour client inspection windows, contractual auto-approvals, KRA eTIMS tax compliance, and automated B2C consultant payouts.

### Associated External Entities
- **Client**
- **Consultant**
- **Kenya Revenue Authority (KRA eTIMS API)**
- **M-Pesa B2C Payout Rail**

### Associated Data Stores
- **D3: Case Studies & Artifacts Datastore**
- **D9: Immutable Escrow & Financial Ledger**
- **D2: Compliance & Audit Vault**
- **D5: Creator Authority & Telemetry Cache**

### Data Flow Analysis (Inputs & Outputs)
| Flow Direction | Data Flow Name / Payload | Source / Origin | Destination |
| :---: | :--- | :--- | :--- |
| $\longleftarrow$ (Inflow) | SOW Proposal & Milestone Definitions | Consultant & Client | `PROC-6.0` |
| $\longleftarrow$ (Inflow) | Milestone Deliverable Files & GitHub PRs | Consultant | `PROC-6.0` |
| $\longleftarrow$ (Inflow) | Milestone Approval + 2FA Confirmation | Client | `PROC-6.0` |
| $\longleftarrow$ (Inflow) | 72-Hour Inspection Countdown Timer Expiry | System Clock | `PROC-6.0` |
| $\longleftarrow$ (Inflow) | Revision Feedback Notes | Client | `PROC-6.0` |
| $\longrightarrow$ (Outflow) | SHA-256 Deliverable Fingerprint & Delivery Timestamp | `PROC-6.0` | D3 / D2 |
| $\longrightarrow$ (Outflow) | Client Review Notification & Countdown Event | `PROC-6.0` | Client |
| $\longrightarrow$ (Outflow) | Statutory KRA eTIMS Electronic Invoice with QR | `PROC-6.0` | KRA API & Client |
| $\longrightarrow$ (Outflow) | Automated B2C Payout Instruction (Net after 7% take rate) | `PROC-6.0` | M-Pesa B2C Rail |
| $\longrightarrow$ (Outflow) | Net Funds & Payout Confirmation | `PROC-6.0` | Consultant |
| $\longrightarrow$ (Outflow) | Milestone State Update ('COMPLETED_RELEASED') | `PROC-6.0` | D9: Escrow Ledger |

### Decomposed Sub-Processes (Level 1 DFD Scope)
| Sub-Process ID | Sub-Process Name | Operational Description |
| :---: | :--- | :--- |
| **6.1** | Initialize Milestone SOW Contract | Binds contractual milestones to escrow funding tranches. |
| **6.2** | Submit & Fingerprint Milestone Deliverable | Computes SHA-256 checksums and begins 72-hour review clock. |
| **6.3** | Process Client Milestone Review & Approval | Captures client acceptance or revision requests. |
| **6.4** | Enforce 72-Hour Contractual Auto-Approval | Automatically clears undisputed deliverables upon timer lapse. |
| **6.5** | Deduct Platform Take Rate & Generate eTIMS Invoice | Calculates 7% commission and queries KRA electronic tax system. |
| **6.6** | Disburse Net Payout via M-Pesa B2C Rails | Transfers net remuneration directly to consultant's phone. |
