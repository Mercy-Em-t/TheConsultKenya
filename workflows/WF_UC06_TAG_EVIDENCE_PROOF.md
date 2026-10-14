# UC-06: Tag Evidence & Proof of Execution
*Diagram Type: Data Flow Diagram (DFD Level 1 - Evidence Verification)*

Traces how proof artifacts (GitHub repos, client co-author confirmations, PDF audit memos, and NDA redaction masks) are verified and attached to a case study.

```mermaid
flowchart LR
    Consultant((Consultant)) -->|1: Repo URL / Client Handle / Asset File| EvidenceHandler[Process Evidence Attachment]
    
    subgraph External Verification Services
        GitHubAPI[GitHub / GitLab REST API]
        ClientUser((Client Co-Author))
    end
    
    subgraph Internal Engine & Vault
        Redactor[NDA Redaction & Blur Engine]
        EvidenceStore[(Encrypted Evidence Vault)]
        CaseStudyStore[(Case Study Database)]
    end
    
    EvidenceHandler -->|2: Query Commits & Stats| GitHubAPI
    GitHubAPI -->|3: Commit SHA, Star Count, Language Stats| EvidenceHandler
    
    EvidenceHandler -->|4: Sign-Off Request Notification| ClientUser
    ClientUser -->|5: Digital Approval Hash| EvidenceHandler
    
    EvidenceHandler -->|6: Raw Image/Doc Containing Sensitive IP| Redactor
    Redactor -->|7: Irreversible Redacted Asset| EvidenceStore
    
    EvidenceHandler -->|8: Compile Evidence Metadata Package| CaseStudyStore
    CaseStudyStore -->|9: Embed Interactive Proof Pills on Post| Consultant
```
