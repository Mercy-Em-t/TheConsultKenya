# Scenario & Jackson-Zave Specification: UC-11

### UC-11: Process Cross-Border Card Payment
* **Requirement ($R_{11}$):** International enterprise clients and diaspora professionals must be able to pay for consulting services in USD, EUR, or GBP via credit/debit cards.
* **Specification ($S_{11}$):**
  * The machine shall support multi-currency selection and convert fees to KES based on live Central Bank of Kenya reference rates.
  * The machine shall tokenize card credentials in compliance with PCI-DSS via Paystack / Flutterwave iframes.
  * The machine shall mandate 3D-Secure 2.0 authentication for all card payments.
* **Assumption ($E_{11}$):**
  * International card issuers allow cross-border e-commerce transactions for professional advisory services.
* **Narrative Scenario ($SC_{11}$):**
  * *Context:* Marcus, an investment director in Zurich, books a Kenyan corporate tax consultation.
  * *Execution:* He selects USD, reviews the live CBK exchange conversion, enters his corporate Visa card, completes his Swiss bank's mobile push authentication, and receives an instant booking receipt in USD with KES equivalent.

---
