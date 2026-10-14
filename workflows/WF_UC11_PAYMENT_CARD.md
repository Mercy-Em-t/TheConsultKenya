# UC-11: Process Cross-Border Card Payment
*Diagram Type: UML Activity Diagram (Multi-Currency Card & 3D-Secure)*

Models multi-currency payment selection, 3D-Secure challenge, tokenization, and Central Bank of Kenya reference exchange conversion.

```mermaid
flowchart TD
    Start([Client Selects Card Payment]) --> SelectCurrency[Select Currency: USD, EUR, GBP, or KES]
    
    SelectCurrency --> CheckCurrency{Is Foreign Currency?}
    CheckCurrency -- Yes --> FetchCBKRate[Fetch Live Central Bank of Kenya Reference FX Rate]
    FetchCBKRate --> DisplayExchange[Display Real-Time FX Rate & Equivalent KES Deposit Amount]
    CheckCurrency -- No --> InputCard[Direct KES Billing]
    DisplayExchange --> InputCard
    
    InputCard --> SubmitCardDetails[Client Submits Cardholder Name, PAN, Expiry, CVV via PCI-DSS Iframe]
    SubmitCardDetails --> GatewayTokenize[Gateway Tokenizes Card & Initiates Charge]
    
    GatewayTokenize --> Check3DS{Requires 3D-Secure Challenge?}
    Check3DS -- Yes --> Launch3DSModal[Render Bank 3D-Secure OTP / App Verification Challenge]
    Launch3DSModal --> CustomerAuth{Customer Authorizes Challenge?}
    
    CustomerAuth -- No / Failed --> ReturnDecline[Gateway Emits Decline Response]
    CustomerAuth -- Yes --> ProcessCharge[Gateway Confirms Successful Charge]
    
    Check3DS -- No --> ProcessCharge
    
    ReturnDecline --> AnalyzeError{Decline Reason}
    AnalyzeError -- Insufficient Funds --> ShowFundingError[Display 'Insufficient funds. Please try another card.']
    AnalyzeError -- Fraud Suspected --> ShowBankContact[Display 'Card blocked by issuing bank. Please notify bank.']
    ShowFundingError --> KeepSlotReserve[Retain Slot Reservation for 5 Minutes & Prompt Card Switch]
    ShowBankContact --> KeepSlotReserve
    
    ProcessCharge --> ConfirmTokenization{Client Opted to Save Card?}
    ConfirmTokenization -- Yes --> StoreToken[Store Secure PCI Token for 1-Click Future Checkout]
    ConfirmTokenization -- No --> SkipToken[Discard Token after Settlement]
    
    StoreToken --> FinalizeBooking[Confirm Slot & Lock Booking in Database]
    SkipToken --> FinalizeBooking
    FinalizeBooking --> IssueReceipt[Dispatch eTIMS Tax Invoice & Calendar Invite]
    IssueReceipt --> Finish([Card Checkout Complete])
```
