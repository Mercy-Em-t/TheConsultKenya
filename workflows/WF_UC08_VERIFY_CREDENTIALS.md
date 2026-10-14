# UC-08: Verify Professional Identity & Credentials
*Diagram Type: UML Activity Diagram (Identity & Multi-Tier Registry Verification)*

Models government identity validation, KRA PIN compliance, professional statutory board verification, and badge issuance.

```mermaid
flowchart TD
    Start([Consultant Enters Verification Settings]) --> SubmitKYC[Submit National ID, Legal Name, and KRA PIN]
    
    SubmitKYC --> CallIPRS[Call National Identity Service / IPRS Gateway]
    CallIPRS --> CheckIDMatch{Identity & KRA PIN Valid?}
    
    CheckIDMatch -- No --> RejectKYC[Display Validation Error & Flag Discrepancy]
    RejectKYC --> PromptRetry[Prompt Consultant to Review Legal Details]
    
    CheckIDMatch -- Yes --> GrantBronze[Grant Bronze Verified Badge: Identity Confirmed]
    GrantBronze --> CheckRegOption{Wishes to Submit Professional Board License?}
    
    CheckRegOption -- No --> CompleteVerification([Tier Finalized: Bronze])
    
    CheckRegOption -- Yes --> SelectBoard{Select Regulatory Board}
    SelectBoard -- Law Society of Kenya --> SubmitLSK[Submit LSK Roll / Practicing Certificate No.]
    SelectBoard -- ICPAK --> SubmitICPAK[Submit ICPAK CPA-K Membership No.]
    SelectBoard -- EBK --> SubmitEBK[Submit Engineers Board of Kenya License No.]
    
    SubmitLSK --> QueryRegAPI[Query Official Statutory Registry]
    SubmitICPAK --> QueryRegAPI
    SubmitEBK --> QueryRegAPI
    
    QueryRegAPI --> CheckStanding{Active Practice Standing Confirmed?}
    CheckStanding -- No --> FlagLicense[Flag License as Inactive/Unverified & Retain Bronze Tier]
    CheckStanding -- Yes --> GrantSilver[Grant Silver Verified Badge & Issue Domain Authority Multiplier]
    
    GrantSilver --> UpdateCAS[Push Update Event to UC-17 CAS Engine]
    UpdateCAS --> CompleteVerification([Tier Finalized: Silver / Gold Candidate])
```
