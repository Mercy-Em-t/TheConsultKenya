# UC-07: Attach Conversion Anchor Call-to-Action
*Diagram Type: UML Activity Diagram (Business Hook Validation)*

Models attaching commercial conversion buttons, screening against external bypass links, and configuring intake parameters.

```mermaid
flowchart TD
    Start([Consultant Enters Step 4: Conversion Anchor]) --> SelectAnchorType{Select Business Action Type}
    
    SelectAnchorType -- Discovery Call --> ConfigDiscovery[Configure 15-Min Discovery Session: Free vs Paid KES]
    SelectAnchorType -- Paid Technical Audit --> ConfigAudit[Configure Deep-Dive Audit: Define Deliverable & Price KES]
    SelectAnchorType -- Download Framework --> ConfigDownload[Upload Framework PDF & Define Email Capture]
    SelectAnchorType -- Retainer Inquiry --> ConfigRetainer[Set Baseline Retainer Scope & Intake Questions]
    
    ConfigDiscovery --> ValidateInput[Run Content Scanner on Anchor Text & Descriptions]
    ConfigAudit --> ValidateInput
    ConfigDownload --> ValidateInput
    ConfigRetainer --> ValidateInput
    
    ValidateInput --> CheckExternalLinks{Contains Phone Number, WhatsApp Link, or External Payment Link?}
    CheckExternalLinks -- Yes --> RejectAnchor[Trigger Validation Error: 'Bypass links prohibited. Use native booking rails.']
    RejectAnchor --> ModifyText[Consultant Cleans Text]
    ModifyText --> ValidateInput
    
    CheckExternalLinks -- No --> BindToProfile[Bind Action Trigger to Consultant Availability Calendar / Escrow Vault]
    BindToProfile --> AttachToPost[Embed Native Sticky Conversion Pill on Final Slide & Header]
    AttachToPost --> FinalPublish[Publish Post to Discovery Feed Engine]
```
