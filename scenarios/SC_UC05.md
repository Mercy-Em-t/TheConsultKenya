# Scenario & Jackson-Zave Specification: UC-05

### UC-05: Compose Case Study via Creation Studio
* **Requirement ($R_{05}$):** Consultants must be able to structure high-value technical deliverables into visually engaging, brand-consistent decks in under 15 minutes without design software.
* **Specification ($S_{05}$):**
  * The machine shall provide 3 narrative frameworks: *Case Study* (*Challenge $\to$ Solution $\to$ Impact*), *Explainer* (*Concept $\to$ Anti-Pattern $\to$ Framework*), and *Toolkit* (*Problem $\to$ Stack $\to$ Checklist*).
  * The machine shall enforce a hard limit of 300 characters per slide and provide a split-screen desktop live preview.
  * The machine shall auto-format markdown, syntax-highlight code snippets, and render Mermaid vector diagrams.
* **Assumption ($E_{05}$):**
  * Restricting unstructured text per slide forces consultants to synthesize high-impact insights rather than dumping unreadable whitepapers.
* **Narrative Scenario ($SC_{05}$):**
  * *Context:* Kiprono, a cloud security specialist, wants to publish a case study on securing mobile banking APIs against SIM-swap attacks.
  * *Execution:* He opens Creation Studio on his laptop, selects "Template A: Case Study", types the challenge on Slide 1, pastes an architecture diagram into Slide 2, and notes the 99.9% fraud reduction impact on Slide 3. The split-screen preview immediately renders a gorgeous, high-contrast carousel. Total drafting time: 8 minutes.

---
