# UC-20: Moderate Platform Content & Enforce NDAs
*Diagram Type: UML Activity Diagram (Content Moderation & IP Protection SLA)*

Models automated text screening for spam/fluff, enterprise NDA breach takedown workflows, and creator appeals.

```mermaid
flowchart TD
    Start([Post Published or Flagged by Community]) --> AutomatedNLP[Execute Automated NLP Filter & Spam Classifier]
    
    AutomatedNLP --> CheckNLPViolation{Violates Quality Standards or Contains Unredacted Fluff?}
    CheckNLPViolation -- Yes --> QuarantinePost[Quarantine Post & Remove from Public Discovery Stream]
    QuarantinePost --> NotifyCreator[Notify Creator with Flagged Excerpts]
    
    CheckNLPViolation -- No --> PostRemainsLive[Post Remains Live on Feed]
    
    PostRemainsLive --> CheckEnterpriseReport{Enterprise Client Files NDA Takedown Request?}
    CheckEnterpriseReport -- Yes --> ExpeditedTakedown[Immediately Hide Post & Trigger 4-Hour SLA Admin Priority Ticket]
    
    ExpeditedTakedown --> AdminAuditsIP[Admin Compares Disputed Asset against Enterprise IP Evidence]
    AdminAuditsIP --> TakedownRuling{Ruling}
    TakedownRuling -- Permanent Breach --> DeletePost[Permanently Delete Post & Deduct Creator Credibility Penalty]
    TakedownRuling -- Redaction Needed --> RequestCreatorRedaction[Return Post to Creator for Forced Redaction]
    TakedownRuling -- No Breach Found --> RestorePost[Restore Post to Feed with Justification Note]
    
    NotifyCreator --> CreatorAppeals{Creator Files Appeal within 7 Days?}
    CreatorAppeals -- Yes --> RouteToHumanMod[Route Appeal to Human Moderation Cockpit]
    RouteToHumanMod --> HumanRuling{Human Moderator Decision}
    HumanRuling -- Approve --> RestorePost
    HumanRuling -- Reject --> ConfirmTakedown[Confirm Takedown & Archive Post]
    CreatorAppeals -- No --> ConfirmTakedown
```
