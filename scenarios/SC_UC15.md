# Scenario & Jackson-Zave Specification: UC-15

### UC-15: Review & Approve Escrow Milestone
* **Requirement ($R_{15}$):** Clients must be able to release funds with 1 click upon satisfaction, while consultants are protected against client abandonment via automated release fallbacks.
* **Specification ($S_{15}$):**
  * Upon client clicking "Approve Deliverable", the machine shall unlock the escrow amount, deduct the 5%–8% platform take rate, and credit the net payout to the consultant wallet within $\le 5\text{s}$.
  * If a client takes zero action for 168 hours (7 days) after submission, the machine shall automatically execute the approval and release funds.
  * The machine shall support instant B2C mobile payouts to the consultant's Safaricom phone in under 30 seconds.
* **Assumption ($E_{15}$):**
  * Clients review deliverables within reasonable business inspection periods.
* **Narrative Scenario ($SC_{15}$):**
  * *Context:* The enterprise reviews Leah’s Phase 1 audit report and finds it exemplary.
  * *Execution:* The director clicks "Approve Deliverable". The system immediately deducts KES 6,000 (6% platform fee), credits KES 94,000 to Leah’s wallet, and dispatches a KRA eTIMS invoice. Leah clicks "Withdraw to M-Pesa" and receives KES 94,000 on her phone within 15 seconds.

---
