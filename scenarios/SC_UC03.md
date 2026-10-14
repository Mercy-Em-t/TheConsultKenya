# Scenario & Jackson-Zave Specification: UC-03

### UC-03: Search & Filter Topic Hubs
* **Requirement ($R_{03}$):** Users searching with conversational or non-technical vocabulary must reliably find verified specialists and relevant industry frameworks.
* **Specification ($S_{03}$):**
  * The machine shall convert input search queries into 128-dimensional dense vectors using the semantic embedder.
  * The machine shall retrieve candidate cards with cosine similarity $\ge 0.65$ within $\le 50\text{ms}$.
  * The machine shall categorize matched results into corresponding topic hubs (`#SoftwareArchitecture`, `#CorporateLaw`, `#TaxStrategy`).
  * If zero exact matches exist, the machine shall return top-rated consultants in the nearest parent discipline.
* **Assumption ($E_{03}$):**
  * Natural language search queries share conceptual semantic overlap with technical case studies even when keyword synonyms diverge.
* **Narrative Scenario ($SC_{03}$):**
  * *Context:* James, a startup founder, searches "how to handle VAT on SaaS sales to Uganda".
  * *Execution:* Despite James not knowing the specific East African Community (EAC) tax treaty codes, the semantic vector search matches two case study decks in the `#TaxStrategy` hub authored by a verified tax accountant explaining cross-border digital service tax, complete with direct booking anchors.

---
