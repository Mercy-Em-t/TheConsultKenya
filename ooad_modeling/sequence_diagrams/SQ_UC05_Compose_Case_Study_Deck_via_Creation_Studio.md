# Sequence Diagram: SQ_UC05 — Compose Case Study Deck via Creation Studio
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC05`  
**Author:** Principal Object Solutions Architect  
**Date:** October 2026  

---

## 1. Interaction Overview & Lifelines
- **Primary Actor:** Initiating user or scheduled daemon trigger.
- **Boundary / UI:** Web interface or modal dialogue receiving keystrokes and rendering feedback.
- **Control / Domain Services:** Orchestrates business invariants and invokes algorithms.
- **Entity / Persistence:** Persistent relational data stores, Redis caches, and S3 vaults.
- **External Gateways:** Third-party integrations (Safaricom Daraja, KRA eTIMS, LiveKit SFU).

---

## 2. UML Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Consultant as 👤 Consultant
    participant StudioUI as 🖥️ MarkdownSplitScreenUI
    participant Parser as ⚙️ StudioParser (PROG-02)
    participant ContentDB as 🗄️ PostgreSQL Database

    Consultant->>StudioUI: Types Markdown with ```mermaid architecture block
    activate StudioUI
    StudioUI->>Parser: compileCaseStudyDeck(rawMarkdown)
    activate Parser
    Parser->>Parser: extractAndRenderMermaid(codeBlock)
    Parser->>Parser: sanitizeHTML(domPurify)
    Parser->>Parser: calculateWordCountAndReadTime()
    Parser-->>StudioUI: compiledView (sanitizedHtml, svgNodes, readTime)
    deactivate Parser
    StudioUI-->>Consultant: Renders Real-Time Live Preview with Vector Diagrams

    Consultant->>StudioUI: Clicks "Publish Case Study"
    StudioUI->>ContentDB: INSERT INTO tbl_case_study_decks (status='PUBLISHED')
    activate ContentDB
    ContentDB-->>StudioUI: deckId (UUIDv7)
    deactivate ContentDB
    StudioUI-->>Consultant: Toast "Published to Authority Network"
    deactivate StudioUI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
