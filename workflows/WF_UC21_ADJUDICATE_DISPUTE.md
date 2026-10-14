# UC-21: Adjudicate Milestone Dispute
*Diagram Type: UML Activity Diagram (Mediation Adjudication & Binding Disbursement)*

Models mediator evidence review across the SOW and SHA-256 asset delivery proofs, binding percentage disbursement rulings, and high-value legal arbitration handoffs.

```mermaid
flowchart TD
    Start([Dispute Escalated from UC-16]) --> AssignMediator[Assign Certified Escrow Mediator / Legal Auditor]
    
    AssignMediator --> OpenAuditCockpit[Open Unified Chronological Audit Cockpit]
    OpenAuditCockpit --> ReviewEvidence[Inspect Signed SOW, SHA-256 Checksums, Deliverable Files & Messages]
    
    ReviewEvidence --> CheckContractValue{Contract Value > KES 1,000,000?}
    CheckContractValue -- Yes --> OfferArbitrationOption[Prompt Parties with CIArb Kenya Formal Arbitration Handoff Option]
    CheckContractValue -- No --> ProceedPlatformRuling[Proceed with Platform Binding Mediation]
    
    OfferArbitrationOption --> OptedCIArb{Either Party Elects CIArb Arbitration?}
    OptedCIArb -- Yes --> TransferToLegalSuspense[Transfer Funds to Legal Suspense Escrow Pending Tribunal Award]
    TransferToLegalSuspense --> EndLegalSuspense([Funds Held Legally])
    
    OptedCIArb -- No --> ProceedPlatformRuling
    
    ProceedPlatformRuling --> MediatorDeterminesFault{Assess Deliverable Compliance against Acceptance Criteria}
    MediatorDeterminesFault -- Work Fully Deficient --> IssueFullRefund[Order 100% Refund to Client Minus Escrow Filing Fee]
    MediatorDeterminesFault -- Work Fully Met SOW --> IssueFullPayout[Order 100% Payout to Consultant Minus Platform Fee]
    MediatorDeterminesFault -- Partial Scope Completed --> IssueSplitRuling[Issue Binding Prorated Ruling: e.g., 70% Refund, 30% Payout]
    
    IssueFullRefund --> ExecuteDisbursement[Escrow Ledger Executes Disbursement to Respective Wallets]
    IssueFullPayout --> ExecuteDisbursement
    IssueSplitRuling --> ExecuteDisbursement
    
    ExecuteDisbursement --> PublishRulingLog[Record Binding Ruling & Justification in Immutable Audit Trail]
    PublishRulingLog --> CloseDispute([Dispute Formally Resolved & Closed])
```
