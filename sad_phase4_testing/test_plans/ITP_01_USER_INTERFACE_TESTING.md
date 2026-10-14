# INTEGRATION TEST PLAN: ITP-01 USER INTERFACE TESTING
**System:** Consult Kenya  
**Integration Category:** Tier 2 — User Interface Integration Testing  
**Test Objective:** Verify that front-end interface components, form controls, navigation menus, modal dialogs, and interactive state widgets coordinate seamlessly with backend API endpoints, preserving context awareness, minimizing user effort, and preventing erroneous submissions.  
**Target Interfaces:** Client Discovery Portal, Consultant Studio & Booking Flow, Escrow Tracking Dashboard, Arbitrator Review Console.  
**Minimum Required Test Scenarios:** 6 (Defined: 6).  

---

## Test Scenarios & Verification Matrix

| Scenario ID | Interface Under Test | User Action & Input Sequence | Expected Integration Behavior | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ITP01-SC-01** | Discovery Search Bar & Category Ribbon | User selects "Tax Law", types "eTIMS compliance", and hits Enter. | Interface triggers debounced query to `/api/v1/search/vector`. Results update dynamically in $<200\text{ms}$ with match highlights and consultant rate cards. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP01-SC-02** | Booking Calendar Modal & Slot Picker | User selects date `2026-11-05`, clicks time slot `14:00`, and proceeds to checkout modal. | Front-end calls `/api/v1/slots/lock`. Slot turns amber with countdown timer (14:59). Checkout modal opens with pre-populated fee summary. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP01-SC-03** | M-Pesa Checkout Dialog | User inputs phone number, clicks "Pay KES 5,000 via M-Pesa", then accidentally clicks button 5 more times. | UI immediately disables button, shows spinner "Waiting for M-Pesa PIN prompt on phone...", suppresses subsequent clicks, opens WebSocket listener. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP01-SC-04** | Keystroke Sequence & Error Recovery | User types invalid email in registration form, attempts tab-navigation to submit, receives inline validation. | Field highlights in crimson with icon, focus trapped until corrected or cancelled. Error message adheres to Phase 3 design guidelines. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP01-SC-05** | LiveKit WebRTC Session Container | Client and Consultant enter `/session/room-CK-8821` at scheduled session time. | UI requests camera/mic permissions, connects to LiveKit SFU room, displays participant video streams, mute controls, and session duration clock. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP01-SC-06** | Dispute Evidence Drag-and-Drop Uploader | Client drags 3 PDF documents and 1 prohibited `.exe` file into dispute drop zone. | UI accepts the 3 valid PDFs, rejects `.exe` with explicit toast alert ("Only PDF, PNG, JPG allowed"), displays upload progress bars. | _Pending — not yet executed_ | **NOT RUN** |

---

## Pass / Fail Summary
- **Execution status:** NOT RUN. This plan has been designed but not yet executed.
- **Observed results:** to be recorded only from actual execution, with a link to the test run / CI job as evidence.
- **Coverage:** to be measured with `pytest --cov` when executed. No coverage figure has been measured yet.

> [!NOTE]
> An earlier version of this file showed observed results and coverage figures that were never measured. They were removed on 13 Oct 2026 (CR-2026-002).
