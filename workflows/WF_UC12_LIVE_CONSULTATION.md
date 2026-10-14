# UC-12: Conduct Secure Live Consultation
*Diagram Type: UML Activity Diagram (WebRTC Media Session & Timekeeping)*

Models live peer-to-peer browser video consultation, interactive screen-sharing, countdown timekeeping, and action item summary generation.

```mermaid
flowchart TD
    Start([Session Time Arrives: T-5 Minutes]) --> EnableJoinButton[Enable 'Join Secure Video Room' on Both Dashboards]
    
    EnableJoinButton --> ClientOrConsultantEnters[Participant Clicks 'Join Secure Video Room']
    ClientOrConsultantEnters --> InitWebRTC[Initialize WebRTC Signaling Server & Check Media Devices]
    InitWebRTC --> EstablishE2EE[Establish Encrypted Peer-to-Peer Media Channel]
    
    EstablishE2EE --> StartSessionClock[Start Consultation Timer & Session Recorder]
    StartSessionClock --> RenderInterface[Render Video Stream, Chat Box & Action Items Sidebar]
    
    RenderInterface --> MeetingEvents{Meeting Events during Session}
    MeetingEvents -- Presenter Shares Screen --> Stream1080p[Broadcast 1080p Screen Stream with Diagram Markup Tools]
    MeetingEvents -- Note Taking --> LogActionItem[Consultant Inputs Key Deliverables / Action Items into Sidebar]
    MeetingEvents -- Clock Reaches T-5 Mins --> TriggerWarning[Trigger Non-Intrusive 5-Minute Overtime Warning Banner]
    
    Stream1080p --> MeetingEvents
    LogActionItem --> MeetingEvents
    
    TriggerWarning --> ClockReachesEnd{Scheduled Time Expires?}
    ClockReachesEnd -- Mutual Extension --> Add15Mins[Both Agree to Extend 15 Mins with Prorated Adjustment]
    ClockReachesEnd -- Wrap Up --> ConcludeSession[Either Party Clicks 'Conclude Consultation']
    Add15Mins --> MeetingEvents
    
    ConcludeSession --> CloseWebRTC[Terminate Peer-to-Peer Media Channels]
    CloseWebRTC --> PromptReview[Prompt Both Parties for Mutual Post-Consultation Rating]
    PromptReview --> DispatchSummary[Email Agreed Action Items & Meeting Summary to Client & Consultant]
    DispatchSummary --> End([Consultation Completed])
```
