# Scenario & Jackson-Zave Specification: UC-09

### UC-09: Book In-App Advisory Consultation
* **Requirement ($R_{09}$):** Clients must be able to schedule consultations in under 4 taps without leaving the application or experiencing double-booking conflicts.
* **Specification ($S_{09}$):**
  * The machine shall open an in-app slide-up bottom sheet over the active content.
  * The machine shall fetch real-time calendar availability from Google/Outlook APIs, applying consultant working hours and buffer times.
  * The machine shall acquire a distributed Redis mutex lock on the chosen slot for 10 minutes upon advancing to checkout.
  * The machine shall mandate completion of a 3-question intake questionnaire before opening payment.
* **Assumption ($E_{09}$):**
  * Consultants keep their connected digital calendars up to date to reflect physical unavailability.
* **Narrative Scenario ($SC_{09}$):**
  * *Context:* Sarah selects a 10:00 AM slot on Thursday for an advisory call with Leah.
  * *Execution:* The system places an invisible 10-minute hold on the slot. Another client browsing Leah’s profile sees that 10:00 AM is temporarily reserved. Sarah completes the 3 intake questions, confirms her mobile number, and proceeds to M-Pesa payment without losing her reservation.

---
