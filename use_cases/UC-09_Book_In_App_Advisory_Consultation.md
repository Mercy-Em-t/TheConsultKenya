# Use Case Specification: Book In-App Advisory Consultation
**Use Case Name:** Book In-App Advisory Consultation | **ID:** `UC-09` | **Priority:** High

**Actor:** Client / Enterprise Buyer
**Description:** The Client books a 1-on-1 advisory consultation with a verified specialist directly from a case study or profile. The system resolves real-time calendar availability, captures pre-intake briefing questions, and reserves the slot pending payment.
**Trigger:** Client clicks 'Book Advisory Consultation' anchor on a case study or profile Bento card.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Client is authenticated (or completes quick SMS OTP verification).
2. Consultant has synchronized external calendar (Google Calendar / Outlook).

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Schedule advisory consultation and reserve slot |  | Booking Initialization |
| **1** | Client clicks 'Book Consultation' anchor | $\longleftarrow$ | Booking CTA Click |
| **2** | System queries Google/Outlook calendar API and presents live interactive availability calendar | $\longrightarrow$ | Live available time slots |
| **3** | Client selects preferred date, time slot, and session duration (e.g., Oct 24, 2:00 PM - 3:00 PM EAT) | $\longleftarrow$ | Selected Date & Slot ID |
| **4** | System places a 15-minute temporary soft lock on the chosen calendar slot | $\longrightarrow$ | 15-minute slot lock |
| **5** | System presents structured intake form: [Consultation Objective, Tech Stack / Legal Domain, Uploaded Docs] | $\longrightarrow$ | Intake questionnaire form |
| **6** | Client completes questionnaire and submits details | $\longleftarrow$ | Client intake responses & attachments |
| **7** | System validates responses and displays payment selection drawer (triggers UC-10 or UC-11) | $\longrightarrow$ | Booking Summary & Fee invoice |

#### Alternative Courses
**9.1 Selected slot is claimed by another user before lock (race condition)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | System detects simultaneous booking conflict during lock | $\longleftarrow$ | Calendar conflict notice |
| 2a | System alerts client: 'Slot was just booked. Showing nearest open alternatives.' | $\longrightarrow$ | Next available slot options |
| 3a | Client picks alternative slot and resumes Normal Course at step 4 | $\longleftarrow$ | Alternative slot pick |

### Postconditions
1. Booking entity created with status 'PENDING_PAYMENT'.
2. Temporary 15-minute reservation held in Redis slot coordinator.
3. Client forwarded to payment checkout.

### Exceptions
**E1: Client abandons checkout / 15-minute timer expires**
1. Redis timer expires without confirmed payment.
2. System automatically releases calendar slot lock and marks booking 'ABANDONED'.
3. Slot becomes instantly available again to the public.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Slot selection, intake form text, attachments | Client Input | Temporary Calendar Slot Lock | Redis Coordination Layer |
| Calendar availability schedule | Google Calendar / Outlook API | Pending Booking Record | Booking Database |
|  |  | Fee Summary Invoice | Client Display |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-009 (Native Booking Engine), FR-010 (M-Pesa STK Integration), FR-011 (Cross-Border Billing)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-09-01: Verify selected slot acquires Redis lock and prevents concurrent double booking.`
- **Boundary & Alternative Test Cases:**
  - `TC-09-02: Test booking across time zones (e.g. Client in London BST booking Nairobi EAT).`
- **Negative & Exception Test Cases:**
  - `TC-09-03: Verify slot lock automatically expires after exactly 900 seconds of inactivity.`
