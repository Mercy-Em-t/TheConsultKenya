# UC-10: Process Payment via M-Pesa STK Push
*Diagram Type: UML Activity Diagram (Fintech STK Push & Reconciliation)*

Models mobile STK dispatch, user PIN entry, asynchronous webhook reconciliation, and Paybill fallback.

```mermaid
flowchart TD
    Start([Client Selects M-Pesa Checkout]) --> InputPhone[Client Inputs Safaricom Phone Number]
    InputPhone --> ValidatePhone{Valid Kenyan Format? e.g., 2547XXXXXXXX}
    
    ValidatePhone -- No --> ShowPhoneError[Display 'Please provide a valid 10-digit mobile number']
    ShowPhoneError --> InputPhone
    
    ValidatePhone -- Yes --> CallSTKGateway[Call Daraja / Paystack M-Pesa STK Push API]
    CallSTKGateway --> StartCountdown[Start 60-Second Client Countdown Timer & Polling Socket]
    
    CallSTKGateway --> PhonePrompt[Safaricom Pushes PIN Prompt to Client Handset]
    PhonePrompt --> UserPINEntry{User Enters Correct M-Pesa PIN?}
    
    UserPINEntry -- No / Cancelled --> WebhookFailure[Gateway Emits Cancellation / Rejection Webhook]
    UserPINEntry -- Timeout (>60s) --> WebhookTimeout[STK Request Expires]
    
    WebhookFailure --> ShowErrorAndRetry[Display 'Transaction Cancelled on Handset']
    WebhookTimeout --> TriggerPaybillFallback[Render Paybill Fallback: Business No, Acc No & 15-Min Timer]
    
    ShowErrorAndRetry --> PromptChoice{Retry STK or Use Paybill?}
    PromptChoice -- Retry STK --> CallSTKGateway
    PromptChoice -- Paybill --> TriggerPaybillFallback
    
    UserPINEntry -- Yes --> SafaricomDebit[Safaricom Debits Client Wallet & Sends B2C Callback]
    SafaricomDebit --> GatewayWebhook[Gateway Dispatches Successful Webhook with Receipt]
    
    GatewayWebhook --> VerifyAmount{Receipt Amount Matches Fee?}
    VerifyAmount -- Yes --> LockSlot[Convert Temporary Slot Lock into Confirmed Booking]
    LockSlot --> CreditEscrow[Hold Funds in Settlement Ledger]
    CreditEscrow --> GenerateInvites[Generate WebRTC Video Link & Send SMS/Calendar Invites]
    GenerateInvites --> CompletePayment([Payment & Booking Confirmed])
```
