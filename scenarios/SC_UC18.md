# Scenario & Jackson-Zave Specification: UC-18

### UC-18: Personalize Two-Pass Discovery Feed
* **Requirement ($R_{18}$):** Users must be served feeds tailored to their active professional challenges, prioritizing local East African market relevance.
* **Specification ($S_{18}$):**
  * **Pass 1:** The machine shall retrieve the top 200 candidate cards using high-dimensional vector cosine similarity within $\le 50\text{ms}$.
  * **Pass 2:** The machine shall rank candidates by multiplying vector similarity $\times$ Creator CAS $\times$ Regional East Africa Multiplier ($1.25\times$), delivering the top 20 cards in $\le 200\text{ms}$.
  * The machine shall inject a 15% exploration quota across diverse disciplines for cold-start users.
* **Assumption ($E_{18}$):**
  * East African enterprises require advisory frameworks grounded in local regulatory and telecommunications realities.
* **Narrative Scenario ($SC_{18}$):**
  * *Context:* An IT director in Kampala logs into Consult Kenya.
  * *Execution:* The Two-Pass AI engine analyzes his interest in cross-border payments. Pass 1 pulls 200 candidates; Pass 2 applies regional East Africa weights and CAS scores, presenting a feed led by top-rated Kenyan and Ugandan fintech architects detailing East African Community interoperability.

---
