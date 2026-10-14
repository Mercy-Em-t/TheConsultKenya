# Use Case Specification: Compose Case Study via Creation Studio
**Use Case Name:** Compose Case Study via Creation Studio | **ID:** `UC-05` | **Priority:** High

**Actor:** Consultant / Specialist Creator
**Description:** The Consultant creates a high-impact, visual-first case study using the modular Creation Studio. The studio provides structured sections (Executive Summary, Challenge, Solution Blueprint, Technical Architecture, Measurable Impact), Markdown/Mermaid diagram rendering, syntax highlighting, and live split-screen preview.
**Trigger:** Consultant clicks '+ Create Case Study' in Creator Dashboard.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Consultant is authenticated and has verified creator permissions.
2. Creation Studio storage and asset CDN are available.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Author and publish structured visual case study |  | Studio Authoring |
| **1** | Consultant selects case study template (e.g. 'Software Architecture Audit', 'Tax Optimization', 'Legal Memo') | $\longleftarrow$ | Selected Template ID |
| **2** | System populates modular editor canvas with structured sections (Challenge, Solution, Impact) | $\longrightarrow$ | Initialized editor canvas |
| **3** | Consultant enters case title, problem statement, and metric callouts (e.g. '99.99% Uptime', 'KES 14M Saved') | $\longleftarrow$ | Case study content & metrics |
| **4** | Consultant embeds Mermaid architecture diagrams or code syntax blocks | $\longleftarrow$ | Mermaid / Code text block |
| **5** | System parses Mermaid syntax and renders live visual diagram in split preview | $\longrightarrow$ | Rendered SVG architecture |
| **6** | System performs automatic auto-save every 30 seconds into draft datastore | $\longrightarrow$ | Draft save state |
| **7** | Consultant previews mobile and desktop responsiveness | $\longleftarrow$ | Preview mode toggle |
| **8** | Consultant clicks 'Proceed to Attach Evidence & CTA' (triggers UC-06 & UC-07) | $\longleftarrow$ | Proceed action |

#### Alternative Courses
**5.1 Syntax error in Mermaid diagram definition (branch at step 5)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | System parser flags syntax error with line number and human-readable suggestion | $\longrightarrow$ | Mermaid parser lint error |
| 2a | Consultant corrects invalid token in editor | $\longleftarrow$ | Corrected diagram text |
| 3a | System re-parses and displays valid SVG diagram | $\longrightarrow$ | Valid rendered diagram |

### Postconditions
1. Draft case study saved in consultant's workspace with unique version identifier.
2. System confirms all assets and diagrams are pre-rendered and cached.

### Exceptions
**E1: Session disconnect or sudden browser close during drafting**
1. Local storage auto-sync recovers last uncommitted keystrokes upon re-opening.
2. Consultant prompted: 'Recover unsaved draft from 2 minutes ago?'

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Template selection & Case study markdown text | Consultant Authoring | Live Rendered SVG / Visual Cards | Editor Preview Canvas |
| Mermaid syntax definitions & Code blocks | Consultant Input | Persisted Draft Document Entity | Creation Studio Database |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-005 (Creation Studio Engine), FR-006 (Diagramming & Code Rendering)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-05-01: Verify valid Mermaid flowchart renders cleanly within 200ms of typing.`
- **Boundary & Alternative Test Cases:**
  - `TC-05-02: Test maximum case study word count (10,000 words) and 15 nested diagrams.`
- **Negative & Exception Test Cases:**
  - `TC-05-03: Verify corrupt markdown does not break client-side layout or crash editor.`
