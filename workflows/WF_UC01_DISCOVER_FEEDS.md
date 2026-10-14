# UC-01: Discover Content via Dual-Mode Feeds
*Diagram Type: UML Activity Diagram (Swimlane Process Flow)*

This workflow models the control logic for client feed scrolling, media prefetching, horizontal carousel swiping, and adaptive network degradation.

```mermaid
flowchart TD
    Start([User Opens App / Selects Home Feed]) --> CheckAuth{Authenticated?}
    CheckAuth -- Yes --> FetchProfile[Fetch User Profile Embeddings & Preferences]
    CheckAuth -- No --> FetchColdStart[Fetch Curated Cold-Start Pool Across Disciplines]
    
    FetchProfile --> Pass1[Trigger Two-Pass AI Retrieval: Pass 1 Candidate Retrieval]
    FetchColdStart --> Pass1
    
    Pass1 --> Pass2[Pass 2: Heavy Business & Regional Ranking]
    Pass2 --> AssembleFeed[Assemble Top 20 Feed Cards]
    
    AssembleFeed --> CheckNetwork{Check Downlink Bandwidth}
    CheckNetwork -- >= 1 Mbps --> HighRes[Pre-render 1080p WebP Slides & Autoplay Muted Video]
    CheckNetwork -- < 1 Mbps --> LowRes[Pre-render 70% WebP Slides & Display Tap-to-Play Video]
    
    HighRes --> RenderFeed[Render Vertical Stream]
    LowRes --> RenderFeed
    
    RenderFeed --> UserGesture{User Gesture Detected}
    UserGesture -- Swipe Up/Down --> ScrollStream[Scroll to Next Vertical Card with <200ms Latency]
    UserGesture -- Swipe Left/Right on Card --> HandleCarousel{Is Multi-Slide Carousel?}
    UserGesture -- Tap Author Avatar --> OpenBento[Transition to UC-02: Bento Grid Profile]
    UserGesture -- Tap Action Button --> OpenAction[Transition to UC-09: Booking Sheet]
    
    HandleCarousel -- Yes --> LockVertical[Lock Vertical Page Scroll Gesture]
    LockVertical --> AdvanceSlide[Advance Slide & Update Progress Scrubber]
    AdvanceSlide --> TrackSlideTelemetry[Record Slide Dwell Time & Index]
    TrackSlideTelemetry --> UnlockScroll[Release Gesture Lock]
    
    HandleCarousel -- No --> RenderFeed
    ScrollStream --> TrackFeedTelemetry[Record Card Impression & Dwell Duration]
    TrackFeedTelemetry --> RenderFeed
```
