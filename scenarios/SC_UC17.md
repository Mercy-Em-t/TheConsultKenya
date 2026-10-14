# Scenario & Jackson-Zave Specification: UC-17

### UC-17: Calculate Creator Authority Score (CAS)
* **Requirement ($R_{17}$):** The platform discovery algorithm must evaluate creators based on verified competence, completed contracts, and peer trust rather than viral social vanity metrics.
* **Specification ($S_{17}$):**
  * The machine shall calculate CAS on a scale of 0.00 to 10.00 based on: Verified Credentials (40%), Completed Escrow Contracts & Ratings (30%), Sanitized Bookmark/Save Telemetry (15%), and Peer Endorsements (15%).
  * The machine shall apply a 5% monthly time-decay to engagement components after 180 days of inactivity.
  * The machine shall quarantine telemetry anomalies detected from bot farms or correlated IPs.
* **Assumption ($E_{17}$):**
  * Real-world professional authority correlates with rigorous statutory licensing, verified enterprise deliveries, and peer practitioner recognition.
* **Narrative Scenario ($SC_{17}$):**
  * *Context:* A newly onboarded lawyer with an active LSK license and 3 completed enterprise escrow contracts publishes a legal framework.
  * *Execution:* The CAS engine computes a score of 8.45/10.00. Her case study receives immediate algorithmic priority in the `#CorporateLaw` hub, outranking superficial unverified posts that had higher view counts.

---
