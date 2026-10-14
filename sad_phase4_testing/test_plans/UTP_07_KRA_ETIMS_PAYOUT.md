# UNIT TEST PLAN: UTP-07 KRA eTIMS INVOICING & AUTOMATED PAYOUTS (PROG-07)
**System:** Consult Kenya  
**Module Target:** `src/app/modules/prog07_kra_etims_payout.py`  
**Test Objective:** Validate tax and payout arithmetic as implemented: **7% platform commission, 5% WHT on gross, 16% VAT on the commission (borne by the platform, inside the commission)**, net payout = gross − commission − WHT. Also validate eTIMS invoice generation, the three-leg ledger posting and B2C payout dispatch.  
**Test Approach:** Hybrid (Black-Box fiscal/arithmetic validation + White-Box branch & precision analysis).  
**Minimum Required Test Cases:** 8 (Defined: 8).  

**Reference calculation (gross KES 10,000):**

| Item | Formula | KES |
| :--- | :--- | ---: |
| Commission | 0.07 × 10,000 | 700.00 |
| of which VAT (platform's liability) | 0.16 × 700 | 112.00 |
| WHT | 0.05 × 10,000 | 500.00 |
| **Net payout** | 10,000 − 700 − 500 | **8,800.00** |

---

## Test Cases Specification & Execution Matrix

| Test Case ID | Test Category | Objective & Input Parameters | Expected Result | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-UTP07-01** | Black-Box (Valid) | Gross KES 10,000; valid KRA PIN `A012345678W`. | Commission 700.00; VAT on commission 112.00; WHT 500.00; net 8,800.00; ledger legs sum to gross. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP07-02** | Black-Box (eTIMS Stub) | Generate signed invoice via eTIMS stub. | Invoice number, signature and QR payload present and stored. (Stub only; real OSCU is tested in ITP-04.) | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP07-03** | Black-Box (Invalid PIN) | KRA PIN `"INVALID_PIN_123"`. | Rejected against pattern `^[AP][0-9]{9}[A-Z]$`; payout not dispatched. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP07-04** | Black-Box (B2C Dispatch) | Approved net KES 8,800 to consultant phone. | B2C request built with correct amount and phone; reference stored. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP07-05** | White-Box (Path) | eTIMS stub raises timeout. | Invoice marked pending sync and queued for retry; payout held until invoice is acknowledged (per design). **Check the code actually does this.** | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP07-06** | White-Box (Branch) | Consultant with WHT exemption certificate. | WHT = 0; net = gross − commission. **Check whether exemption is implemented; if not, log a CR.** | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP07-07** | Black-Box (Boundary) | Batch settlement of 3 receipts. | `total_wht_remitted_kes` and `total_net_payouts_kes` equal the sums of individual receipts. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP07-08** | White-Box (Precision) | Gross amounts that stress rounding: 1,234.57; 0.01; 999,999.99; and 1,000 random amounts. | For every amount: commission + WHT + net == gross **exactly** (no 1-cent drift). **Expected to fail or be fragile:** code uses `float` + `round()`, not `Decimal` (CR-2026-006). | _Pending — not yet executed_ | **NOT RUN** |

---

## Pass / Fail Summary
- **Execution status:** NOT RUN. This plan has been designed but not yet executed.
- **Observed results:** to be recorded only from actual execution, with a link to the test run / CI job as evidence.
- **Coverage:** to be measured with `pytest --cov` when executed. No coverage figure has been measured yet.

> [!NOTE]
> An earlier version of this file used a 10% commission (the approved requirement is 5–8%, implemented as 7%), claimed `Decimal` precision the code doesn't use, and showed observed results that were never measured. It was corrected on 13 Oct 2026 (CR-2026-001, CR-2026-002, CR-2026-006).
