# UC-19: Manage Phased Rollout & Creator Onboarding
*Diagram Type: UML Activity Diagram (Phase Transition & Access Gate Control)*

Models platform progression across Phase 1 (Anchor Agency lockdown), Phase 2 (Curated Cohort invite codes), and Phase 3 (Open Multi-Tenant onboarding).

```mermaid
flowchart TD
    Start([Admin Enters Platform Governance Cockpit]) --> QueryPhase{Current Global Platform Phase?}
    
    QueryPhase -- Phase 1: Anchor Agency --> Phase1Mode[Lock Creation Studio Exclusively to Proprietary Consulting Agency Accounts]
    Phase1Mode --> PublicUserHitsStudio{Public User Attempts to Publish?}
    PublicUserHitsStudio -- Yes --> ShowP1Banner[Display 'Platform in Closed Beta. Join Founding Waitlist' Page]
    PublicUserHitsStudio -- No --> AgencyPublishes[Agency Accounts Publish Initial Architecture Decks]
    
    QueryPhase -- Phase 2: Curated Cohort --> Phase2Mode[Activate Invitation Code Engine]
    Phase2Mode --> AdminIssuesCodes[Admin Generates Cryptographic Codes for 25 Selected Specialist Peers]
    AdminIssuesCodes --> PeerRedeemsCode[Invited Specialist Enters Code during Registration]
    PeerRedeemsCode --> ValidateCode{Code Valid & Unused?}
    ValidateCode -- No --> RejectCode[Reject Registration & Prompt Valid Invite]
    ValidateCode -- Yes --> GrantFoundingBadge[Grant 'Founding Creator' Badge & Unlock Studio Access]
    
    QueryPhase -- Phase 3: Open Ecosystem --> Phase3Mode[Open Self-Service Onboarding Directory Across East Africa]
    Phase3Mode --> PublicApplies[Open Application Pipeline with Automated Credential & KYC Gates]
    PublicApplies --> EnableMultiTenancy[Enable Multi-Tenant Firm Accounts & Pro SaaS Portals]
    
    GrantFoundingBadge --> MonitorQuality[Admin Monitors Feed Content Quality & Algorithmic Calibration]
    EnableMultiTenancy --> ScalePlatform([Platform Scaling in Open Ecosystem])
```
