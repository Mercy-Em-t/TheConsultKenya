# Sequence Diagram: SQ_UC06 — Tag Evidence and Proof of Execution
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC06`  
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
    participant UI as 🖥️ EvidenceUploaderUI
    participant EvidenceCtrl as ⚙️ EvidenceController
    participant Vault as 🗄️ Amazon S3 KMS Vault
    participant DB as 🗄️ tbl_evidence_proofs

    Consultant->>UI: Uploads Audit Memo PDF / Deliverable Proof
    activate UI
    UI->>EvidenceCtrl: uploadProof(fileStream, proofType='AUDIT_MEMO_PDF')
    activate EvidenceCtrl
    EvidenceCtrl->>EvidenceCtrl: computeSHA256Checksum(fileStream)
    EvidenceCtrl->>Vault: putObject(bucket="consultkenya-proofs", fileStream, KMS)
    activate Vault
    Vault-->>EvidenceCtrl: artifactUrl
    deactivate Vault
    EvidenceCtrl->>DB: INSERT INTO tbl_evidence_proofs (checksum, artifactUrl, proofType)
    activate DB
    DB-->>EvidenceCtrl: proofId (UUID)
    deactivate DB
    EvidenceCtrl-->>UI: returnProofBadge(proofId, checksum)
    deactivate EvidenceCtrl
    UI-->>Consultant: Renders Verified Proof Badge on Case Study Card
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
