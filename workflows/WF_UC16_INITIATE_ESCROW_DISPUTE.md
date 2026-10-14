# UC-16: Initiate Escrow Dispute & Mediation
*Diagram Type: UML Activity Diagram (Dispute Escalation & Evidence Freezing)*

Models freezing funds upon deliverable contestation, mutual 48-hour evidence submission, amicable settlement, and formal mediation handoff.

```mermaid
flowchart TD
    Start([Dispute Raised by Client or Consultant]) --> FreezeEscrow[Freeze Milestone Escrow Balance & Halt Auto-Release Clocks]
    FreezeEscrow --> UpdateContractStatus[Mark Contract Status as 'In Formal Dispute']
    
    UpdateContractStatus --> OpenMediationPortal[Initialize Secure Mediation Ticket & Thread]
    OpenMediationPortal --> Start48HourClock[Start 48-Hour Evidence Submission Countdown]
    
    Start48HourClock --> PartiesSubmitEvidence[Both Parties Upload Signed SOW, Chat Logs & Deliverable Diff]
    
    PartiesSubmitEvidence --> CheckAmicableSettlement{Can Parties Agree to Mutual Split?}
    CheckAmicableSettlement -- Yes --> ExecuteMutualSplit[Both Parties Sign Prorated Agreement: e.g. 60% Refund, 40% Payout]
    ExecuteMutualSplit --> DistributeFunds[System Distributes Agreed Split Automatically]
    DistributeFunds --> CloseTicket([Dispute Amicably Resolved])
    
    CheckAmicableSettlement -- No --> EscalateToMediator[Escalate Ticket to Platform Escrow Mediator / Legal Auditor]
    EscalateToMediator --> TransitionToUC21[Transition to UC-21: Adjudicate Milestone Dispute]
```
