# User Scenario: Escrow Dispute Mediation & Legal Adjudication
**Scenario ID:** `SCEN-04` | **Persona:** Senior Counsel Otieno, Appointed Platform Escrow Mediator

### Business Goal
Adjudicate an unresolvable scope dispute between an enterprise client and a consultant for Milestone 3.

### Initial Preconditions & Environmental Context
Otieno logs into the Mediator Adjudication Workspace on desktop Chrome.

### Step-by-Step User Interaction Narrative
1. Opens 'Dispute Queue'; selects Case #DISP-2026-088; escrow balance is displayed as FROZEN (KES 180,000).
2. Interface presents three-pane legal workspace: Left (SOW Contract & Acceptance Clauses), Center (Delivered Code Artifacts & Commit History), Right (Client Claim vs. Consultant Rebuttal Dossier).
3. Otieno uses the interactive diff tool to identify that 3 out of 5 required endpoints were implemented to specification.
4. Navigates to 'Adjudication Verdict' tab; selects 'Prorated Settlement'; adjusts slider to 60% Consultant (KES 108,000) and 40% Client Refund (KES 72,000).
5. Inputs legal rationale citing Contract Clause 8.2 in the formatted decision text box.
6. Digitally signs ruling using hardware security key; system unfreezes escrow, executes disbursement, and generates sealed Adjudication Certificate PDF.

### UI / UX Ergonomic Implications
Three-pane dense legal layout, synchronized scrolling across contract and diffs, and precise numeric percentage sliders with instant currency recomputation.