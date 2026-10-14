# CONSULT KENYA: USER & DEVELOPER TUTORIALS
**Document Type:** Formal System Tutorial & Guided Learning Document  
**Audience:** End-Users (Clients & Consultants) and Third-Party System Developers  
**Lifecycle Stage:** Phase 4 — Implementation & Onboarding  
**Version:** 1.0 (Production Master)  

---

## 1. Table of Contents & Navigation Index

- [1. Table of Contents & Navigation Index](#1-table-of-contents--navigation-index)
- [2. Learning Path & Pedagogical Structure](#2-learning-path--pedagogical-structure)
- [3. End-User Guided Walkthroughs](#3-end-user-guided-walkthroughs)
  - [3.1 [Search Advisory] Finding the Right Tax or Legal Expert in 60 Seconds](#31-search-advisory-finding-the-right-tax-or-legal-expert-in-60-seconds)
  - [3.2 [Reserve Slot] Booking a Session and Paying with Safaricom M-Pesa](#32-reserve-slot-booking-a-session-and-paying-with-safaricom-m-pesa)
  - [3.3 [Join Room] Attending a High-Definition Advisory Consultation](#33-join-room-attending-a-high-definition-advisory-consultation)
- [4. Developer & Integrator Tutorials](#4-developer--integrator-tutorials)
  - [4.1 [Integrate API] 5-Minute Developer Quickstart with Python and cURL](#41-integrate-api-5-minute-developer-quickstart-with-python-and-curl)
  - [4.2 [Simulate Webhook] Local Testing of M-Pesa STK Push and Callbacks](#42-simulate-webhook-local-testing-of-m-pesa-stk-push-and-callbacks)
  - [4.3 [Verify Receipt] Validating KRA eTIMS Fiscal Invoices Programmatically](#43-verify-receipt-validating-kra-etims-fiscal-invoices-programmatically)
- [5. Two-Part Navigation Index & Keyword Directory](#5-two-part-navigation-index--keyword-directory)

---

## 2. Learning Path & Pedagogical Structure
These tutorials follow an active learning framework designed to build confidence in using and integrating Consult Kenya:
- **Prerequisites & Concept:** Why the step exists and what to expect.
- **Hands-On Action:** Clear, concrete actions with exact UI clicks or terminal commands.
- **Expected Feedback:** What visual or API response confirms success.
- **Troubleshooting Tip:** How to recover if something unexpected occurs.

---

## 3. End-User Guided Walkthroughs

### 3.1 [Search Advisory] Finding the Right Tax or Legal Expert in 60 Seconds

#### Objective
Discover a verified advocate or tax consultant specializing in your exact problem statement using our natural-language semantic vector search.

#### Step 1: Navigate to Search Portal
Open your browser and navigate to `https://consultkenya.co.ke/`. You will see the visual discovery interface with category pills and the unified search bar.

#### Step 2: Formulate Your Query
Instead of generic keywords like *"lawyer"*, type your actual business scenario:
> *"Need advice on transferring ancestral land in Kiambu with missing succession grant"*

#### Step 3: Review Ranked Matches
Within 150 milliseconds, the two-pass AI engine returns matching experts ranked by relevance. Notice:
- The **Authority Badge** (e.g., *LSK Advocate — 12 Years Standing*).
- The **Video Introduction**: Click the 30-second video thumbnail to see and hear the consultant explain their approach before spending a single shilling.

```
+-------------------------------------------------------------+
|  Adv. Grace Mwangi            [VERIFIED LSK ADVOCATE]       |
|  Land Law & Succession Specialist, Kiambu & Nairobi         |
|  Rating: 4.97 (48 reviews)    Hourly Rate: KES 8,000        |
|  [ Play 30s Video Intro ]     [ View Available Slots -> ]   |
+-------------------------------------------------------------+
```

---

### 3.2 [Reserve Slot] Booking a Session and Paying with Safaricom M-Pesa

#### Objective
Reserve an open advisory slot and fund the milestone escrow using your Safaricom mobile phone.

#### Step 1: Select Your Preferred Time
On the consultant profile, click **Book Advisory Session**. An interactive weekly calendar appears. Click an available slot (e.g., `Thursday, 14:00 - 15:00`).

#### Step 2: Review Escrow Protection Notice
A slide-out drawer appears displaying:
- **Consultation Fee:** KES 8,000.00
- **Escrow Guarantee:** *"Your funds are held securely by Consult Kenya and are only released after your session is completed and deliverable approved."*

#### Step 3: Authorize via M-Pesa
1. Enter your Safaricom mobile number (e.g., `0712345678`).
2. Click **Deposit to Escrow**.
3. Keep your phone screen unlocked. Within 3 seconds, a SIM toolkit prompt will appear on your phone:
   ```
   Do you want to pay KES 8,000.00 to CONSULT KENYA ACC: CK-BKG-8812?
   Enter M-Pesa PIN: [ **** ]
   ```
4. Enter your PIN and press OK.
5. The webpage will immediately update to **Booking Confirmed!** and dispatch calendar invites to your email and WhatsApp.

---

### 3.3 [Join Room] Attending a High-Definition Advisory Consultation

#### Objective
Join your private, encrypted LiveKit WebRTC video consultation room.

#### Step 1: Access the Session Link
At the scheduled consultation time, open the SMS or email notification and click **Join Advisory Session**, or navigate to your Client Dashboard.

#### Step 2: System Check
The browser will prompt for camera and microphone access. Click **Allow**. Verify that your audio levels register on the green volume meter.

#### Step 3: Conduct Your Session
Click **Enter Room**. You are now in a private, end-to-end encrypted video room with your advisor. You can:
- Share your screen to review land titles, financial models, or contracts.
- Download deliverables uploaded directly into the session chat.
- When finished, click **End Call**.

---

## 4. Developer & Integrator Tutorials

### 4.1 [Integrate API] 5-Minute Developer Quickstart with Python and cURL

#### Objective
Query the Consult Kenya API to retrieve consultant availability and create bookings programmatically from an external enterprise ERP.

#### Step 1: Obtain API Bearer Token
```bash
curl -X POST "https://api.consultkenya.co.ke/api/v1/auth/token" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
  }'
```
*Expected Response:*
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### Step 2: Execute Vector Search via Python
```python
import requests

API_URL = "https://api.consultkenya.co.ke/api/v1/search/vector"
TOKEN = "YOUR_ACCESS_TOKEN"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "query": "Corporate restructuring and transfer pricing tax audit",
    "top_k": 3
}

response = requests.post(API_URL, json=payload, headers=headers)
results = response.json()

for consultant in results.get("matches", []):
    print(f"Expert: {consultant['name']} | Rate: KES {consultant['hourly_rate_kes']}")
```

---

### 4.2 [Simulate Webhook] Local Testing of M-Pesa STK Push and Callbacks

#### Objective
Test the payment and escrow lifecycle locally using our pre-built Daraja simulation harness without requiring a real Safaricom merchant account.

#### Step 1: Trigger Simulated STK Push
Run the local CLI test script:
```powershell
python -m src.app.modules.prog05_mpesa_daraja --simulate-push --phone 254712345678 --amount 5000
```

#### Step 2: Inject Simulated Success Webhook Callback
Send a POST request to your local webhook endpoint:
```bash
curl -X POST "http://localhost:8000/api/v1/payments/mpesa/callback" \
  -H "Content-Type: application/json" \
  -d '{
    "Body": {
      "stkCallback": {
        "MerchantRequestID": "9812-441-1",
        "CheckoutRequestID": "ws_CO_1210202620450091823",
        "ResultCode": 0,
        "ResultDesc": "The service request is processed successfully.",
        "CallbackMetadata": {
          "Item": [
            {"Name": "Amount", "Value": 5000.00},
            {"Name": "MpesaReceiptNumber", "Value": "QHD78129KJ"},
            {"Name": "TransactionDate", "Value": 20261012204500},
            {"Name": "PhoneNumber", "Value": 254712345678}
          ]
        }
      }
    }
  }'
```
*Expected Server Log:*
```
[INFO] M-Pesa Callback verified: Receipt QHD78129KJ | Milestone transitioned to FUNDED_LOCKED
```

---

### 4.3 [Verify Receipt] Validating KRA eTIMS Fiscal Invoices Programmatically

#### Objective
Retrieve and verify the cryptographic fiscal signature on a consultation invoice for corporate tax filing.

```python
import requests

INVOICE_URL = "https://api.consultkenya.co.ke/api/v1/payouts/invoices/INV-2026-00491"
headers = {"Authorization": "Bearer YOUR_TOKEN"}

res = requests.get(INVOICE_URL, headers=headers).json()
print("KRA Control Code:", res["kra_control_code"])
print("Fiscal Signature:", res["fiscal_signature"])
print("QR Code URL:     ", res["qr_verification_url"])
```

---

## 5. Two-Part Navigation Index & Keyword Directory

| Two-Part Term (Action + Subject) | Tutorial Link | Audience |
| :--- | :--- | :--- |
| **[Integrate API]** | [Section 4.1](#41-integrate-api-5-minute-developer-quickstart-with-python-and-curl) | Backend Software Engineers |
| **[Join Room]** | [Section 3.3](#33-join-room-attending-a-high-definition-advisory-consultation) | Clients & Consultants |
| **[Reserve Slot]** | [Section 3.2](#32-reserve-slot-booking-a-session-and-paying-with-safaricom-m-pesa) | New Clients |
| **[Search Advisory]** | [Section 3.1](#31-search-advisory-finding-the-right-tax-or-legal-expert-in-60-seconds) | All Users |
| **[Simulate Webhook]** | [Section 4.2](#42-simulate-webhook-local-testing-of-m-pesa-stk-push-and-callbacks) | Integrators & QA Engineers |
| **[Verify Receipt]** | [Section 4.3](#43-verify-receipt-validating-kra-etims-fiscal-invoices-programmatically) | Corporate Accountants & CFOs |
