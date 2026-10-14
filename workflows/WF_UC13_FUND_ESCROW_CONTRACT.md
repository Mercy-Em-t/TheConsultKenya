# UC-13: Fund Milestone Escrow Contract
*Diagram Type: UML Activity Diagram (B2B Contract Phasing & Deposit Locking)*

Models Statement of Work (SOW) milestone drafting, digital signatures, escrow deposit locking, and project kickoff.

```mermaid
flowchart TD
    Start([Parties Conclude Initial Discovery]) --> ConsultantDraftsSOW[Consultant Drafts Phased SOW: Milestones, Budgets & Acceptance Criteria]
    
    ConsultantDraftsSOW --> SubmitToClient[Submit Draft to Client Workspace]
    SubmitToClient --> ClientReviewsSOW{Client Accepts SOW Terms?}
    
    ClientReviewsSOW -- Requests Edits --> RequestAmendments[Client Adds Amendment Notes on Scope / Deliverables]
    RequestAmendments --> ConsultantDraftsSOW
    
    ClientReviewsSOW -- Accepts --> DigitalSign[Both Parties Digitally Sign Agreement via Cryptographic Key Hash]
    DigitalSign --> GenerateContractLedger[Generate Immutable Contract Record in Escrow Ledger]
    
    GenerateContractLedger --> ClientFundsM1[Client Initiates Funding for Milestone 1: M-Pesa / Card / Bank Wire]
    ClientFundsM1 --> PaymentGateway[Process Deposit via Payment Rail]
    
    PaymentGateway --> CheckDeposit{Deposit Cleared?}
    CheckDeposit -- No --> PromptRetryFunding[Prompt Client for Alternative Payment Method]
    PromptRetryFunding --> ClientFundsM1
    
    CheckDeposit -- Yes --> LockInEscrowVault[Lock Principal in Platform Escrow Trust Vault]
    LockInEscrowVault --> TransitionStatus[Update Milestone Status to 'Funded & In Progress']
    TransitionStatus --> NotifyConsultant[Notify Consultant: Funds Guaranteed, Safe to Commence Execution]
    NotifyConsultant --> StartExecution([Milestone 1 Active])
```
