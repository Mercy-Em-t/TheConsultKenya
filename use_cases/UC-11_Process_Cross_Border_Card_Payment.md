# Use Case Specification: Process Cross-Border Card Payment
**Use Case Name:** Process Cross-Border Card Payment | **ID:** `UC-11` | **Priority:** Medium

**Actor:** Client / Enterprise Buyer (Diaspora / International)
**Description:** The Client pays for services using international credit/debit cards (Visa, Mastercard, American Express). The payment is processed via 3D Secure 2.0 with automated currency conversion to Kenyan Shillings (KES).
**Trigger:** Client selects 'Credit / Debit Card' on checkout drawer.
**Type:** [x] External  [ ] Temporal

### Preconditions
1. Booking or escrow milestone is in 'PENDING_PAYMENT'.
2. International payment gateway (Paystack / Flutterwave / Stripe) is operational.

---
### Execution Steps & Information Flow
*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*

#### Normal Course
| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| **1.0** | Process card payment with 3D Secure verification |  | Card Processing |
| **1** | Client enters Cardholder Name, 16-digit Card Number, Expiry, and CVV | $\longleftarrow$ | Card credentials (tokenized) |
| **2** | Client-side library tokenizes card data directly to PCI-DSS Level 1 gateway | $\longrightarrow$ | Card Token |
| **3** | Gateway initiates 3D Secure challenge (OTP / Bank App authentication) | $\longrightarrow$ | 3DS Challenge Modal |
| **4** | Client confirms challenge with issuing bank | $\longleftarrow$ | 3DS Authentication |
| **5** | Gateway executes fund capture and emits successful charge webhook to platform | $\longleftarrow$ | Charge Success Webhook |
| **6** | System locks equivalent KES amount in milestone escrow and generates tax invoice | $\longrightarrow$ | Escrow confirmation & invoice |

#### Alternative Courses
**11.1 Card declined (insufficient funds, fraud block, or expired card)**

| Step | Action / Activity Performed | Flow | Information for Step |
| :--- | :--- | :---: | :--- |
| 1 | Gateway returns decline error code (e.g. 'card_declined', 'insufficient_funds') | $\longleftarrow$ | Decline error payload |
| 2a | System displays user-friendly bank decline explanation and prompts for alternative card | $\longrightarrow$ | Decline UI notification |

### Postconditions
1. Funds locked into escrow vault.
2. Booking status transitions to 'CONFIRMED'.

### Exceptions
**E1: 3D Secure authentication timeout or failure**
1. Gateway voids pending authorization.
2. Booking remains pending payment with slot preserved for 5 minutes.

---
### Summary Inputs & Outputs
| Summary Inputs | Source | Outputs | Destination |
| :--- | :--- | :--- | :--- |
| Tokenized card data | Client Browser | Card Charge Token | Payment Gateway API |
| Charge success webhook payload | Paystack / Flutterwave Gateway | Confirmed Booking Record | Booking Database |

---
### Systems Analysis Traceability & Verification
**Correlated Functional Requirements:** FR-011 (Cross-Border Multi-Currency Billing), FR-013 (Escrow Ledger Management)

**Testing Strategy & Acceptance Test Cases:**
- **Positive Test Cases (Normal Course):**
  - `TC-11-01: Verify 3DS 2.0 flow successfully executes and records exchange rate at transaction time.`
- **Boundary & Alternative Test Cases:**
  - `TC-11-02: Test high-value international transaction ($5,000 USD) with fraud screening.`
- **Negative & Exception Test Cases:**
  - `TC-11-03: Verify zero card details (PAN/CVV) touch platform application servers (PCI-DSS audit compliance).`
