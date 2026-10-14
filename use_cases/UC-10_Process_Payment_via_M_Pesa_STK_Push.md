# Use Case Specification: Process Payment via M-Pesa STK Push
**Use Case Name:** Process Payment via M-Pesa STK Push | **ID:** `UC-10` | **Priority:** High

**Actor:** Client / Enterprise Buyer
**Description:** The Client pays for a consultation booking or milestone escrow contract using M-Pesa mobile money. The platform triggers an instant Safaricom Daraja STK Push to the user's mobile device, verifies PIN authorization, and locks funds in escrow.
**Trigger:** Client selects 'M-Pesa' as payment method on the checkout drawer and clicks 'Pay Now'.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Booking or escrow contract is in 'PENDING_PAYMENT' state.
2. Safaricom Daraja API gateway is operational.
3. Client has an active Safaricom line with sufficient balance.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Execute M-Pesa mobile payment via Daraja STK Push |  | Payment Execution |
| **1** | Client enters Safaricom mobile phone number (e.g. 0712345678) and confirms fee amount | $\longleftarrow$ | Phone number & Amount |
| **2** | System sanitizes phone number into international format (+254712345678) | $\longrightarrow$ | Normalized phone number |
| **3** | System issues Lipa Na M-Pesa Online STK Push request to Safaricom Daraja API | $\longrightarrow$ | Daraja STK payload |
| **4** | Client's mobile handset receives on-screen prompt: 'Do you want to pay KES 10,000 to KenyaConsult?' | $\longrightarrow$ | Safaricom USSD / SIM Prompt |
| **5** | Client inputs secret M-Pesa PIN on handset and submits | $\longleftarrow$ | Encrypted PIN submission |
| **6** | Safaricom validates funds and delivers asynchronous Callback to platform webhook URL | $\longleftarrow$ | Daraja Callback JSON payload |
| **7** | System verifies callback signature, transaction code (e.g. 'RJK894KL9'), and exact amount paid | $\longleftarrow$ | M-Pesa Transaction Code |
| **8** | System transitions booking status from 'PENDING_PAYMENT' to 'CONFIRMED_ESCROW_LOCKED' | $\longrightarrow$ | Updated Booking Entity |
| **9** | System dispatches instant SMS and email receipt with encrypted calendar invite to both parties | $\longrightarrow$ | Receipt & Calendar Invite |

#### Alternative Courses
**10.1 Client cancels prompt on handset or enters incorrect PIN**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Safaricom delivers failure callback with ResultCode 1032 ('Request cancelled by user') | $\longleftarrow$ | Cancellation Callback |
| 2a | System updates checkout screen: 'Payment cancelled on handset. Try again or choose Card payment.' | $\longrightarrow$ | Retry Prompt UI |
| 3a | Client taps 'Retry M-Pesa' or selects Card | $\longleftarrow$ | User Retry Choice |

**10.2 Insufficient balance on M-Pesa account**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Safaricom callback indicates ResultCode 1 ('Insufficient funds') | $\longleftarrow$ | Insufficient Funds Code |
| 2a | System notifies client to top up M-Pesa or switch payment methods | $\longrightarrow$ | Insufficient funds alert |

### Postconditions
1. Transaction recorded in KenyaConsult double-entry financial ledger.
2. Funds deposited into platform trust escrow account.
3. Calendar booking finalized and WebRTC room generated (triggers UC-12).

### Exceptions
**E1: Daraja webhook callback delayed or network timeout (>60 seconds)**
1. Platform initiates active Daraja Transaction Status Query polling endpoint.
2. Upon receiving positive query response, platform reconciles transaction and confirms booking.
3. If query times out after 3 minutes, client is prompted to enter M-Pesa SMS transaction code for automated manual matching.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Phone number & Consultation Fee | Client Checkout Form | STK Push Request | Safaricom Daraja API |
| Daraja Callback JSON payload | Safaricom Payment Gateway | Confirmed Booking & Escrow Receipt | Client & Consultant |
|  |  | Financial Ledger Record | Platform Accounting System |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-010 (M-Pesa STK Push Integration), FR-013 (Escrow Ledger Management), FR-022 (Tax & eTIMS Compliance)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-10-01: Verify successful Daraja callback (ResultCode 0) updates booking to CONFIRMED within 3 seconds.`
- **Boundary & Alternative Test Cases:**
  - `TC-10-02: Test maximum single transaction limit (KES 250,000 per CBK/Safaricom limits).`
- **Negative & Exception Test Cases:**
  - `TC-10-03: Verify idempotency—duplicate callbacks with same M-Pesa code do not create duplicate ledger entries.`
