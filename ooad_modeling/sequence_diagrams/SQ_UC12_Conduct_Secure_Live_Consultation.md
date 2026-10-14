# Sequence Diagram: SQ_UC12 — Conduct Secure Live Consultation
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Sequence Modeling  
**Associated Use Case:** `UC12`  
**Author:** Principal Object Solutions Architect  
**Date:** October 2026  

---

## 1. Interaction Overview & Lifelines
- **Primary Actor:** Initiating user or scheduled daemon trigger.
- **Boundary / UI:** Web interface or modal dialogue receiving keystrokes and rendering feedback.
- **Control / Domain Services:** Orchestrates business invariants and invokes algorithms.
- **Entity / Persistence:** Persistent relational data stores, Redis caches, and S3 vaults.
- **External Gateways:** Third-party integrations (Safaricom Daraja, KRA eTIMS, LiveKit SFU).

---

## 2. UML Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Client as 👤 Client
    actor Consultant as 👤 Consultant
    participant UI as 🖥️ WebRTCSessionRoom
    participant SessionCtrl as ⚙️ LiveSessionController
    participant LiveKit as 🏛️ LiveKit Cloud SFU Gateway

    Client->>UI: Joins /session/room-CK-8821
    Consultant->>UI: Joins /session/room-CK-8821
    activate UI
    UI->>SessionCtrl: requestRoomTokens(userId, bookingId)
    activate SessionCtrl
    SessionCtrl->>SessionCtrl: verifyBookingStatusConfirmed(bookingId)
    SessionCtrl->>SessionCtrl: issueLiveKitJWT(roomName="room-CK-8821", ttl=5400)
    SessionCtrl-->>UI: accessTokensPair
    deactivate SessionCtrl

    UI->>LiveKit: WSS Connect & Join Room (PeerConnection)
    activate LiveKit
    LiveKit-->>UI: WebRTC Media Channels Established (Opus Audio / VP9 Video)
    deactivate LiveKit
    
    Note over Client,Consultant: Advisory session conducted with screen share and note-taking
    
    Consultant->>UI: Clicks "End Advisory Call"
    UI->>SessionCtrl: recordSessionEnd(bookingId, durationMins=58)
    activate SessionCtrl
    SessionCtrl->>SessionCtrl: updateStatus("COMPLETED")
    SessionCtrl-->>UI: SessionConcludedReceipt()
    deactivate SessionCtrl
    UI-->>Client: Prompts for Rating & Deliverable Approval
    deactivate UI
```

---

## 3. Message Sequence Table & Operational Descriptions
1. **Message Invariants:** All requests carry typed DTO parameters and are validated at boundary.
2. **Asynchronous Execution:** Background jobs (e.g. Celery CAS recalculation, Daraja callbacks) operate non-blocking.
3. **Transactional Guarantees:** Financial ledger state mutations execute within atomic, serializable database transactions.
