# Scenario & Jackson-Zave Specification: UC-16

### UC-16: Initiate Escrow Dispute & Mediation
* **Requirement ($R_{16}$):** If delivered work fails agreed SOW specifications, parties must be able to halt automated releases and enter a formal evidence-backed dispute process.
* **Specification ($S_{16}$):**
  * Upon dispute filing, the machine shall immediately freeze milestone escrow funds and pause all auto-approval countdown timers.
  * The machine shall provide a 48-hour mutual evidence submission portal for both parties to upload documentation.
  * The machine shall enable parties to execute an amicable prorated split without third-party intervention.
* **Assumption ($E_{16}$):**
  * Commercial disputes can often be resolved through mutual compromise once communication is structured around written evidence.
* **Narrative Scenario ($SC_{16}$):**
  * *Context:* A client discovers that an external API integration deliverable is missing required SACCO endpoints.
  * *Execution:* The client clicks "Raise Dispute". Payout timers freeze instantly. Through the mediation portal, both parties discuss the omission and mutually agree to a 75/25 split release, resolving the issue without waiting for formal mediation.

---
