# UC-05: Compose Case Study via Creation Studio
*Diagram Type: UML Activity Diagram (Authoring & Validation Engine)*

Models the 4-step creation studio: format selection, narrative template drafting, character validation, and live preview rendering.

```mermaid
flowchart TD
    Start([Consultant Taps Center '+' Create Button]) --> CheckPermissions{Authorized Creator?}
    CheckPermissions -- No (Phase 1/2 Unvetted) --> ShowAccessNotice[Display 'Join Founding Cohort' Prompt]
    
    CheckPermissions -- Yes --> Step1[Step 1: Format Selection: Carousel, Micro-Video, or Blueprint Card]
    Step1 --> SelectTemplate{Select Narrative Template}
    
    SelectTemplate -- Template A --> LoadCaseStudy[Load 'Challenge -> Solution -> Impact' Shell]
    SelectTemplate -- Template B --> LoadExplainer[Load 'Concept -> Anti-Pattern -> Best Practice' Shell]
    SelectTemplate -- Template C --> LoadToolkit[Load 'Problem -> Recommended Stack -> Checklist' Shell]
    
    LoadCaseStudy --> ComposeSlide[Consultant Types Slide Content / Pastes Code Snippet]
    LoadExplainer --> ComposeSlide
    LoadToolkit --> ComposeSlide
    
    ComposeSlide --> ValidateCharCount{Character Count <= 300 per slide?}
    ValidateCharCount -- No --> HighlightError[Highlight Overrun in Red & Disable 'Next' Button]
    HighlightError --> PruneText[Consultant Prunes Text]
    PruneText --> ValidateCharCount
    
    ValidateCharCount -- Yes --> UpdateLivePreview[Update Interactive Split-Screen Live Preview]
    UpdateLivePreview --> CheckDiagramCode{Contains Mermaid/Code Block?}
    CheckDiagramCode -- Yes --> RenderSyntaxDiagram[Render Syntax Highlight & Vector Architecture Diagram]
    CheckDiagramCode -- No --> CheckSlideCount{All Slides Completed?}
    RenderSyntaxDiagram --> CheckSlideCount
    
    CheckSlideCount -- Add Another Slide --> ComposeSlide
    CheckSlideCount -- Ready for Step 2 --> NextStep[Advance to UC-06: Tag Evidence & Proof]
```
