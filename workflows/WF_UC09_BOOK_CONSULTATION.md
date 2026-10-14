# UC-09: Book In-App Advisory Consultation
*Diagram Type: UML Activity Diagram (Native Scheduling & Slot Reservation)*

Models native slide-up sheet rendering, dynamic calendar availability fetch, 10-minute slot locking, and questionnaire completion.

```mermaid
flowchart TD
    Start([Client Taps 'Book Consultation' Anchor on Post]) --> TriggerSheet[Trigger Native In-App Slide-Up Sheet without Page Redirect]
    
    TriggerSheet --> FetchAvailability[Query Consultant Connected Calendars: Google / Outlook API]
    FetchAvailability --> FilterBuffers[Apply Consultant Working Hours, Buffer Times & Daily Caps]
    FilterBuffers --> RenderCalendar[Render Next 14 Days Open Slots in Client Local Time Zone]
    
    RenderCalendar --> ClientSelectsSlot[Client Selects Specific Date & Time Slot]
    ClientSelectsSlot --> CheckRaceLock{Attempt Distributed 10-Min Mutex Lock on Slot}
    
    CheckRaceLock -- Lock Failed (Already Held) --> ShowSlotUnavailable[Display 'Slot just reserved by another user. Please choose another.']
    ShowSlotUnavailable --> RenderCalendar
    
    CheckRaceLock -- Lock Acquired --> SetTempReservation[Set 10-Minute Temporary Reservation in Redis/DB]
    SetTempReservation --> RenderIntake[Render Mandatory 3-Question Intake Questionnaire]
    
    RenderIntake --> ClientSubmitsAnswers[Client Completes Answers & Clicks 'Proceed to Payment']
    ClientSubmitsAnswers --> ValidateAnswers{All Mandatory Fields Answered?}
    
    ValidateAnswers -- No --> PromptIncomplete[Highlight Required Fields]
    PromptIncomplete --> RenderIntake
    
    ValidateAnswers -- Yes --> DeterminePayment{Free Discovery or Paid Consultation?}
    DeterminePayment -- Free Discovery --> AutoConfirm[Generate Calendar Invite & Meeting WebRTC Room Link]
    DeterminePayment -- Paid Consultation --> LaunchPayment[Trigger UC-10: M-Pesa STK or UC-11: Card Rails]
    
    AutoConfirm --> CompleteBooking([Session Confirmed & Dispatched])
```
