# Scenario & Jackson-Zave Specification: UC-10

### UC-10: Process Payment via M-Pesa STK Push
* **Requirement ($R_{10}$):** Kenyan clients must be able to execute frictionless, instant payment for consultations via their mobile phones using Safaricom M-Pesa.
* **Specification ($S_{10}$):**
  * The machine shall call Daraja / Paystack APIs to dispatch an STK push prompt to the client's phone within $\le 5\text{s}$.
  * The machine shall listen for the webhook callback and confirm the booking within $\le 2\text{s}$ of receipt.
  * The machine shall enforce idempotency based on `MpesaReceiptNumber`.
  * If the STK prompt times out after 60 seconds, the machine shall render Paybill manual payment instructions with a 15-minute dynamic reference code.
* **Assumption ($E_{10}$):**
  * The client has sufficient M-Pesa balance on their SIM card and enters their secret 4-digit PIN accurately.
* **Narrative Scenario ($SC_{10}$):**
  * *Context:* Sarah confirms her KES 15,000 consultation booking.
  * *Execution:* Her phone screen illuminates with an M-Pesa prompt: "Do you want to pay KES 15,000 to Consult Kenya?". She inputs her PIN. Two seconds later, the web screen updates with confetti: "Booking Confirmed! Google Meet link dispatched to your calendar."

---
