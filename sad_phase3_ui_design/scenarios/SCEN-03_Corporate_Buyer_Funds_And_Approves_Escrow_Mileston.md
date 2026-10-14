# User Scenario: Corporate Buyer Funds & Approves Escrow Milestone Deliverable
**Scenario ID:** `SCEN-03` | **Persona:** Amina Hassan, Head of Procurement at an East African Logistics Conglomerate

### Business Goal
Review a delivered customs clearance automation blueprint and disburse KES 250,000 milestone funds.

### Initial Preconditions & Environmental Context
Amina receives an SMS and email notification that Milestone 2 has been submitted by the consultant.

### Step-by-Step User Interaction Narrative
1. Taps deep link in email on her iPad; authenticates via FaceID into the Escrow Management portal.
2. Milestone dashboard displays 72-hour inspection countdown timer with amber status indicator.
3. Inspects submitted artifacts (ZIP archive, SHA-256 fingerprint, and deployment URL) in the inline file previewer.
4. Verifies deliverable against SOW acceptance criteria checklist.
5. Clicks green primary button: 'Approve Milestone & Release Funds'.
6. Confirmation modal summarizes financial settlement: Milestone Total (KES 250,000), 7% Platform Fee (KES 17,500), Net Consultant Payout (KES 232,500), and KRA Withholding Tax deduction.
7. Enters SMS OTP verification code; system displays green success checkmark, generates KRA eTIMS invoice with QR code, and triggers M-Pesa B2C payout.

### UI / UX Ergonomic Implications
Critical financial transparency: fee deductions must be unmistakably clear; irreversible approval actions must require explicit 2FA modal confirmation.