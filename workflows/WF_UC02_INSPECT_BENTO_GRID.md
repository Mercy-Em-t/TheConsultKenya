# UC-02: Inspect Consultant Portfolio (Bento Grid)
*Diagram Type: UML Activity Diagram (Due Diligence & Layout Switch)*

Models the inspection flow when a client lands on a consultant's profile, including the 5-second authority audit and view mode switching.

```mermaid
flowchart TD
    Start([Client Taps Consultant Profile]) --> QueryProfile[Query Consultant Record & Credential Tier]
    QueryProfile --> CheckStatus{Account Active?}
    CheckStatus -- No / Suspended --> ShowSuspended[Display 'Profile Suspended / Inactive' Notice]
    
    CheckStatus -- Yes --> FetchBlocks[Fetch Execution Blocks, Case Studies, Ratings & CAS Score]
    FetchBlocks --> CheckCount{Has Published Blocks?}
    
    CheckCount -- No --> RenderPlaceholder[Render Cold-Start Portfolio: Verified Badges & Bio Placeholder]
    CheckCount -- Yes --> RenderBentoGrid[Render Bento Grid: Flagship Tiles, Rating Summary, Sticky Book Button]
    
    RenderBentoGrid --> UserAction{User Action on Profile}
    UserAction -- Tap Project Tile --> ExpandCaseStudy[Expand Fullscreen Case Study Overlay with Telemetry]
    UserAction -- Toggle View Switch --> SwitchMode{Selected Mode}
    UserAction -- Tap Sticky CTA --> LaunchBooking[Trigger UC-09: Slide-Up Booking Modal]
    UserAction -- Tap Credential Badge --> ViewCredVerification[Display IPRS / LSK / GitHub Verification Proof]
    
    SwitchMode -- Timeline Feed --> RenderChronological[Switch to Chronological Stream View without Full Reload]
    SwitchMode -- Visual Grid --> RenderBentoGrid
    
    ExpandCaseStudy --> ViewSlides[Browse Full Slides / Architecture Blueprints]
    ViewSlides --> CloseOrConvert{Convert or Dismiss?}
    CloseOrConvert -- Convert --> LaunchBooking
    CloseOrConvert -- Dismiss --> RenderBentoGrid
```
