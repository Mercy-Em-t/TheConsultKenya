# Program Specification: MpesaDarajaPaymentAndCallbackCoordinator
**Program ID:** `PROG-05` | **Module Type:** Fintech Transaction & Ingress Gateway
**Language / Framework:** `Python 3.12 / FastAPI / Celery / Cryptography`

### Description
Initiates Safaricom Lipa Na M-Pesa Online (STK Push) queries, validates incoming asynchronous webhook callback signatures, prevents duplicate replay attacks, and transitions booking and escrow states.

### Systems Design Characteristics
- **Cohesion Type:** Sequential Cohesion (Output of STK push initiation feeds directly into callback verification pipeline)
- **Coupling Level:** Data Coupling (Cryptographic callback JSON DTO)
- **Fan-In:** `3` (High reuse by upstream callers)
- **Fan-Out:** `4` (Optimal controlled subordinate delegations)

### Associated Events & Triggers
- `EVT-PAY-MPESA-SUBMIT: Client clicks 'Pay via M-Pesa'.`
- `EVT-DARAJA-CALLBACK-POST: Safaricom gateway delivers transaction webhook.`

### Program Input Parameters
| Input Parameter | Data Transfer Object (DTO) | Internal Elements |
| :--- | :--- | :--- |
| **`payment_init`** | `PaymentInitDTO` | booking_id, phone_number, amount_kes |
| **`daraja_callback`** | `DarajaCallbackPayloadDTO` | MerchantRequestID, CheckoutRequestID, ResultCode, CallbackMetadata |

### Program Output Returns
| Output Return | Data Transfer Object (DTO) | Internal Elements |
| :--- | :--- | :--- |
| **`stk_response`** | `STKPushResponseDTO` | CheckoutRequestID, ResponseCode, CustomerMessage |
| **`reconciliation_status`** | `PaymentReconciliationDTO` | transaction_code, escrow_status, ledger_entry_id |

### Detailed Algorithmic Pseudocode
```python
FUNCTION ProcessDarajaCallback(callback_payload: JSON) -> ReconciliationResult:
    INPUT: callback_payload (Body.stkCallback)
    OUTPUT: ReconciliationResult

    stk_data = callback_payload["Body"]["stkCallback"]
    checkout_id = stk_data["CheckoutRequestID"]
    result_code = stk_data["ResultCode"]

    // 1. Idempotency Guard (Prevent double-processing of replayed webhooks)
    IF Redis.Exists("processed_daraja:" + checkout_id) THEN
        RETURN ReconciliationResult(status="ALREADY_PROCESSED")
    END IF

    // 2. Locate Pending Booking / Escrow Record
    booking = Database.Bookings.FindByCheckoutID(checkout_id)
    IF booking IS NULL THEN
        RAISE OrphanedTransactionException("No booking mapped to CheckoutID: " + checkout_id)
    END IF

    // 3. Evaluate Safaricom Result Code
    IF result_code == 0 THEN
        // SUCCESSFUL TRANSACTION
        metadata = ParseCallbackMetadata(stk_data["CallbackMetadata"])
        mpesa_receipt = metadata["MpesaReceiptNumber"] // e.g., 'RJK894KL9'
        amount_paid = metadata["Amount"]

        BEGIN TRANSACTION
            // Post Double-Entry Journal Entry
            ledger_id = DoubleEntryLedgerService.PostTransaction(
                debit_account="ESCROW_TRUST_CASH",
                credit_account="CLIENT_DEPOSIT_LIABILITY",
                amount=amount_paid,
                reference=mpesa_receipt,
                rail="MPESA_DARAJA"
            )

            // Update Booking State
            Database.Bookings.UpdateStatus(booking.id, "CONFIRMED_ESCROW_LOCKED")
            
            // Release Slot Lock (Promoted to permanent booking)
            Redis.Delete("slot_lock:" + booking.consultant_id + ":" + booking.start_time)

            // Mark Webhook Processed in Redis with 72-hour TTL
            Redis.Set("processed_daraja:" + checkout_id, mpesa_receipt, EX=259200)
        COMMIT TRANSACTION

        // Asynchronously notify client & consultant with calendar invite
        CeleryWorker.EnqueueTask("DispatchBookingConfirmationNotice", booking.id)
        
        RETURN ReconciliationResult(status="SUCCESS", receipt=mpesa_receipt)
    ELSE
        // TRANSACTION CANCELLED OR INSUFFICIENT FUNDS
        Database.Bookings.UpdateStatus(booking.id, "PAYMENT_FAILED", Reason=stk_data["ResultDesc"])
        RETURN ReconciliationResult(status="FAILED", error=stk_data["ResultDesc"])
    END IF
END FUNCTION
```
