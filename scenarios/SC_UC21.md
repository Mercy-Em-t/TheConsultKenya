# Scenario & Jackson-Zave Specification: UC-21

### UC-21: Adjudicate Milestone Dispute
* **Requirement ($R_{21}$):** When parties cannot settle an escrow dispute, a neutral mediator must issue an enforceable ruling based on documented evidence.
* **Specification ($S_{21}$):**
  * The machine shall present all signed SOW clauses, SHA-256 asset delivery timestamps, and communication logs in a unified audit dashboard.
  * The machine shall execute binding fund splits (0%–100%) as directed by the mediator's authenticated ruling.
  * For contracts $> \text{KES } 1,000,000$, the machine shall support escrow transfer into legal suspense pending formal CIArb Kenya tribunal awards.
* **Assumption ($E_{21}$):**
  * Digital contracts and immutable cryptographic evidence logs are recognized as admissible evidence under the Kenya Information and Communications Act (KICA) and Evidence Act.
* **Narrative Scenario ($SC_{21}$):**
  * *Context:* A client and consultant deadlock over a KES 200,000 systems architecture deliverable.
  * *Execution:* The escrow mediator reviews the SOW and inspects the SHA-256 stamped files. The mediator notes that 80% of required diagrams were delivered to standard, but deployment scripts were omitted. The mediator issues an authoritative ruling: 80% payout (KES 160k) to consultant, 20% refund (KES 40k) to client. The system executes disbursements instantly.

---
