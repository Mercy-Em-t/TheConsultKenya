# Scenario & Jackson-Zave Specification: UC-14

### UC-14: Submit Project Milestone Deliverable
* **Requirement ($R_{14}$):** Consultants must submit finished deliverables with irrefutable proof of delivery timestamps and cryptographic tamper protection.
* **Specification ($S_{14}$):**
  * The machine shall compute a SHA-256 checksum across all uploaded deliverable assets and write the hash and ISO-8601 timestamp into the immutable audit ledger.
  * The machine shall start a 72-hour formal inspection countdown timer for the client.
  * The machine shall allow consultants to request deadline extensions without penalty if submitted before the milestone due date.
* **Assumption ($E_{14}$):**
  * Uploaded deliverable files represent the complete scope of agreed milestone work.
* **Narrative Scenario ($SC_{14}$):**
  * *Context:* Leah completes Phase 1 of the governance audit.
  * *Execution:* She uploads the 45-page audit report PDF. The system computes SHA-256 hash `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, records it in the ledger, and notifies the client that the 72-hour review period has begun.

---
