# Business Process Specification: Schedule & Conduct Live Advisory Consultations
**Process ID:** `PROC-4.0` | **Owner:** Client / Consultant / Video Engine

### Description
Orchestrates direct calendar slot reservation, 15-minute temporary coordination locks, intake question capture, and zero-friction WebRTC video conference delivery.

### Associated External Entities
- **Client**
- **Consultant**
- **External Calendar Services (Google/Outlook)**
- **WebRTC Video Media Server**

### Associated Data Stores
- **D1: User & Credential Registry**
- **D6: Bookings & Consultation Datastore**
- **D10: Active Slot Locks & Coordination Cache**

### Data Flow Analysis (Inputs & Outputs)
| Flow Direction | Data Flow Name / Payload | Source / Origin | Destination |
| :---: | :--- | :--- | :--- |
| $\longleftarrow$ (Inflow) | Availability calendar query & slot selection | Client | `PROC-4.0` |
| $\longleftarrow$ (Inflow) | External calendar busy/free blocks | Calendar Services API | `PROC-4.0` |
| $\longleftarrow$ (Inflow) | Pre-consultation briefing responses & files | Client | `PROC-4.0` |
| $\longleftarrow$ (Inflow) | WebRTC media streams & shared notes | Client & Consultant | `PROC-4.0` |
| $\longleftarrow$ (Inflow) | Session termination signal | Client / Consultant | `PROC-4.0` |
| $\longrightarrow$ (Outflow) | 15-Minute Slot Lock Reservation | `PROC-4.0` | D10: Active Slot Locks |
| $\longrightarrow$ (Outflow) | Pending Booking Record & Fee Invoice | `PROC-4.0` | D6: Bookings DB |
| $\longrightarrow$ (Outflow) | Confirmed Calendar Invites with Room Tokens | `PROC-4.0` | Client, Consultant & Calendar API |
| $\longrightarrow$ (Outflow) | Encrypted Peer-to-Peer A/V Session | `PROC-4.0` | Client & Consultant |
| $\longrightarrow$ (Outflow) | Session Duration Telemetry & Summary PDF | `PROC-4.0` | D6 / Participant Email |

### Decomposed Sub-Processes (Level 1 DFD Scope)
| Sub-Process ID | Sub-Process Name | Operational Description |
| :---: | :--- | :--- |
| **4.1** | Synchronize Real-Time Calendar Availability | Queries external calendar providers to display unconflicted slots. |
| **4.2** | Coordinate Slot Soft-Locking & Intake Capture | Enforces 15-minute Redis reservation while collecting client briefs. |
| **4.3** | Finalize Booking & Generate Meeting Access Tokens | Binds confirmed payment to cryptographic WebRTC room tokens. |
| **4.4** | Establish Encrypted WebRTC Live Session | Coordinates DTLS-SRTP peer media streaming and shared scratchpad. |
| **4.5** | Monitor Session Telemetry & Handle No-Shows | Logs call duration and executes automated no-show policy. |
