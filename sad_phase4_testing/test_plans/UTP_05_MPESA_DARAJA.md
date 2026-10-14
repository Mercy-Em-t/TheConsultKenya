# UNIT TEST PLAN: UTP-05 M-PESA DARAJA STK PUSH & WEBHOOK COORDINATOR (PROG-05)
**System:** Consult Kenya  
**Module Target:** `src/app/modules/prog05_mpesa_daraja.py`  
**Test Objective:** Validate end-to-end integration with Safaricom Daraja APIv2: STK Push initiation, password hashing (BusinessShortCode + Passkey + Timestamp), webhook callback signature verification, duplicate webhook idempotency, and timeout/cancellation status tracking.  
**Test Approach:** Hybrid (Black-Box Webhook Payload Injection + White-Box Cryptographic & Idempotency Key Coverage).  
**Minimum Required Test Cases:** 8 (Defined: 8).  

---

## Test Cases Specification & Execution Matrix

| Test Case ID | Test Category | Objective & Input Parameters | Expected Result | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-UTP05-01** | Black-Box (Valid) | Trigger STK Push: Amount KES 5,000, Phone `254712345678`, AccountRef `CK-BKG-8801`. | Generates Base64 auth token, sends JSON payload to Safaricom Daraja, receives `ResponseCode: 0`, returns `MerchantRequestID` and `CheckoutRequestID`. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP05-02** | Black-Box (Callback Success) | Webhook callback arrives: `ResultCode: 0`, `MpesaReceiptNumber: QHD78129KJ`, Amount 5000.00. | Webhook decrypted, status updated from `PENDING` to `COMPLETED`, escrow deposit event fired, client notified via SMS/WebSocket. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP05-03** | Black-Box (User Cancel) | Webhook callback arrives: `ResultCode: 1032` (Request cancelled by user on USSD prompt). | Transaction marked `CANCELLED_BY_USER`. Slot lock freed. Client UI displays cancellation guidance. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP05-04** | Black-Box (Timeout) | Webhook callback arrives: `ResultCode: 1037` (DS timeout / subscriber phone off). | Transaction marked `EXPIRED_TIMEOUT`. Slot unlocked. Retry option offered to user. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP05-05** | Black-Box (Idempotency) | Duplicate webhook: Safaricom delivers the identical callback payload twice within 200ms. | Second callback hits idempotency barrier (`CheckoutRequestID` already processed). Returns HTTP 200 to Safaricom without duplicate credit or double-booking. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP05-06** | Black-Box (Boundary) | Payment amount KES 1.00 (Minimum Daraja test amount) vs KES 250,000.00 (Per-transaction M-Pesa limit) vs KES 250,001.00. | KES 1: Accepted. KES 250,000: Accepted. KES 250,001: Rejected with validation error ("Amount exceeds Safaricom single transaction limit"). | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP05-07** | White-Box (Attack) | Forged callback without valid HMAC signature or coming from non-Safaricom IP. | Origin check & signature verification fails. Returns HTTP 401 Unauthorized. Security alert logged. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP05-08** | White-Box (Mutation) | Negative monetary amount (`-1000.00 KES`) injected into request model. | Pydantic validator `gt=0` raises validation error. Daraja API is never called. | _Pending — not yet executed_ | **NOT RUN** |

---

## Pass / Fail Summary
- **Execution status:** NOT RUN. This plan has been designed but not yet executed.
- **Observed results:** to be recorded only from actual execution, with a link to the test run / CI job as evidence.
- **Coverage:** to be measured with `pytest --cov` when executed. No coverage figure has been measured yet.

> [!NOTE]
> An earlier version of this file showed observed results and coverage figures that were never measured. They were removed on 13 Oct 2026 (CR-2026-002).
