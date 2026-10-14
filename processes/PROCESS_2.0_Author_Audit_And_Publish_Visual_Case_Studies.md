# Business Process Specification: Author, Audit & Publish Visual Case Studies
**Process ID:** `PROC-2.0` | **Owner:** Consultant / Compliance Officer / Moderation Daemon

### Description
Governs the authoring lifecycle of structured case studies in Creation Studio, rendering Mermaid SVG diagrams, attaching cryptographic execution proofs, configuring conversion CTAs, and automated Data Loss Prevention (DLP) moderation.

### Associated External Entities
- **Consultant**
- **Compliance Officer**
- **External Code Repositories (GitHub/GitLab)**

### Associated Data Stores
- **D3: Case Studies & Artifacts Datastore**
- **D4: Evidence & Execution Proofs Vault**
- **D2: Compliance & Audit Vault**

### Data Flow Analysis (Inputs & Outputs)
| Flow Direction | Data Flow Name / Payload | Source / Origin | Destination |
| :---: | :--- | :--- | :--- |
| $\longleftarrow$ (Inflow) | Modular narrative markdown & metrics | Consultant | `PROC-2.0` |
| $\longleftarrow$ (Inflow) | Mermaid architecture syntax & code blocks | Consultant | `PROC-2.0` |
| $\longleftarrow$ (Inflow) | Proof URLs, commit hashes, audit PDFs | Consultant | `PROC-2.0` |
| $\longleftarrow$ (Inflow) | Commit verification payloads | GitHub / GitLab API | `PROC-2.0` |
| $\longleftarrow$ (Inflow) | Moderation & Redaction directives | Compliance Officer | `PROC-2.0` |
| $\longrightarrow$ (Outflow) | Live Rendered SVG Diagrams & Split-Screen Preview | `PROC-2.0` | Consultant Display |
| $\longrightarrow$ (Outflow) | SHA-256 Proof Fingerprint & Verified Badges | `PROC-2.0` | D4 / Case Study |
| $\longrightarrow$ (Outflow) | Sanitized Published Case Study Deck | `PROC-2.0` | D3: Case Studies Datastore |
| $\longrightarrow$ (Outflow) | DLP Security Alert & Moderation Dossier | `PROC-2.0` | Compliance Officer / D2 |

### Decomposed Sub-Processes (Level 1 DFD Scope)
| Sub-Process ID | Sub-Process Name | Operational Description |
| :---: | :--- | :--- |
| **2.1** | Draft Modular Case Study Sections | Parses Problem, Architecture Blueprint, Implementation, and Quantified Impact. |
| **2.2** | Compile Architecture Diagrams & Code Blocks | Generates real-time interactive SVG renderings from textual Mermaid syntax. |
| **2.3** | Verify & Digest Execution Proofs | Validates external repo commits and computes immutable SHA-256 digests. |
| **2.4** | Bind Native Conversion Anchor CTA | Configures embedded booking drawers and advisory fee structures. |
| **2.5** | Scan for DLP Confidentiality & Redact IP | Applies regex scanners for credentials and sensitive client trade secrets. |
