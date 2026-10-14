# UC-14: Submit Project Milestone Deliverable
*Diagram Type: UML Activity Diagram (Asset Submission & SHA-256 Proof Generation)*

Models milestone deliverable asset upload, cryptographic hashing, inspection timer initialization, and deadline extension exceptions.

```mermaid
flowchart TD
    Start([Consultant Completes Milestone Work]) --> CheckDeadline{Deadline Approaching?}
    
    CheckDeadline -- Need More Time --> RequestExtension[Submit Deadline Extension Request with Rationale]
    RequestExtension --> ClientExtensionReview{Client Approves Extension?}
    ClientExtensionReview -- Yes --> UpdateDeadline[Update Milestone Due Date without Penalty]
    ClientExtensionReview -- No --> ProceedSubmission[Proceed with Immediate Submission]
    UpdateDeadline --> ProceedSubmission
    
    CheckDeadline -- On Track --> ProceedSubmission
    
    ProceedSubmission --> UploadAssets[Consultant Uploads Deliverables: PDFs, Code Repos, Schemas]
    UploadAssets --> ComputeSHA256[Compute SHA-256 Cryptographic Checksum across All Assets]
    ComputeSHA256 --> WriteSummary[Consultant Writes Technical Completion Summary & Changelog]
    
    WriteSummary --> FinalizeSubmission[Click 'Submit Deliverable for Client Inspection']
    FinalizeSubmission --> SaveVault[Save Assets to Project Locker & Record SHA-256 Hash on Escrow Ledger]
    
    SaveVault --> Start72HourTimer[Initialize 72-Hour Inspection Countdown Timer]
    Start72HourTimer --> NotifyClient[Notify Client: Milestone Submitted for Formal Review]
    NotifyClient --> TransitionToReview([Milestone in Review Phase])
```
