# UC-15: Review & Approve Escrow Milestone
*Diagram Type: UML Activity Diagram (Approval, Auto-Release & B2C Disbursement)*

Models client inspection, deliverable sign-off, take-rate deduction, instant B2C M-Pesa payout, and 7-day auto-approval fallback.

```mermaid
flowchart TD
    Start([Milestone Enters Inspection Window]) --> ClientInspects[Client Inspects Submitted Deliverables & SHA-256 Hashes]
    
    ClientInspects --> InspectionTimer{72-Hour Timer Elapsed?}
    InspectionTimer -- Active --> ClientDecision{Client Action}
    
    ClientDecision -- Request Revision --> SubmitRevisionNotes[Submit Specific Scope Revision Notes to Consultant]
    SubmitRevisionNotes --> ResetInspection[Consultant Amends & Re-submits Deliverable]
    ResetInspection --> ClientInspects
    
    ClientDecision -- Raise Dispute --> EscalateDispute[Transition to UC-16: Initiate Escrow Dispute]
    
    ClientDecision -- One-Click Approve --> TriggerRelease[Client Clicks 'Approve Deliverable']
    
    InspectionTimer -- Timer Reached 168 Hours (7 Days) with Zero Client Action --> AutoApproval[System Triggers 7-Day Auto-Approval Fallback]
    
    TriggerRelease --> UnlockVault[Unlock Escrow Funds in Platform Trust Ledger]
    AutoApproval --> UnlockVault
    
    UnlockVault --> DeductTakeRate[Calculate & Deduct 5%-8% Platform Fee to Operating Account]
    DeductTakeRate --> GenerateETIMS[Trigger UC-22: Generate KRA eTIMS Tax Invoice]
    GenerateETIMS --> CreditConsultantWallet[Credit Net Payout to Consultant Escrow Wallet]
    
    CreditConsultantWallet --> ConsultantWithdrawal{Consultant Requests Payout?}
    ConsultantWithdrawal -- Instant M-Pesa --> CallB2CRails[Call Safaricom B2C API: Mobile Payout Dispatched in <30s]
    ConsultantWithdrawal -- Commercial Bank EFT --> ScheduleEFT[Queue EFT / RTGS Transfer for Next Banking Day]
    ConsultantWithdrawal -- Hold in Wallet --> HoldBalance[Retain Balance for Future Direct Withdrawals]
    
    CallB2CRails --> CompleteDisbursement([Milestone Settled & Completed])
    ScheduleEFT --> CompleteDisbursement
    HoldBalance --> CompleteDisbursement
```
