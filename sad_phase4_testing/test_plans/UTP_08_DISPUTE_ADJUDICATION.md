# UNIT TEST PLAN: UTP-08 DISPUTE ARBITRATION & ADJUDICATION (PROG-08)
**System:** Consult Kenya  
**Module Target:** `src/app/modules/prog08_dispute_adjudication.py`  
**Test Objective:** Validate dispute case intake, evidence dossier uploading, arbitration state machine, split refund calculation, and mutual settlement agreements.  
**Test Approach:** Hybrid (Black-Box Dispute Resolution Paths + White-Box Evidence Validation & Split Arithmetic).  
**Minimum Required Test Cases:** 8 (Defined: 8).  

---

## Test Cases Specification & Execution Matrix

| Test Case ID | Test Category | Objective & Input Parameters | Expected Result | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-UTP08-01** | Black-Box (Valid) | Client files dispute on milestone `M-301` within 7 days of delivery: Reason: `"Deficient legal opinion"`, evidence attachment `contract_defects.pdf`. | Dispute created with status `OPEN_UNDER_REVIEW`. Milestone locked. 48-hour response timer initiated for consultant. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP08-02** | Black-Box (Late Filing) | Client files dispute after 14 days (Statute of limitations is 7 days post-delivery). | Rejection with HTTP 400 ("Dispute window has elapsed for this milestone"). | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP08-03** | Black-Box (Adjudication Split) | Arbitrator rules: 60% Refund to Client, 40% Payout to Consultant on KES 50,000 escrow. | Escrow disbursed: KES 30,000 refunded to Client via M-Pesa B2C, KES 20,000 (less taxes/fees) to Consultant. Status $\rightarrow$ `RESOLVED_SPLIT`. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP08-04** | Black-Box (Mutual Amicable) | Parties agree on mutual cancellation with 100% refund before consultant has commenced work. | Instant transition to `MUTUALLY_CANCELLED`. 100% principal refunded to client. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP08-05** | White-Box (Branch) | Consultant fails to submit counter-evidence within 48-hour deadline. | Cron job marks consultant `DEFAULTED_NO_RESPONSE`. System auto-rules in favor of client. Full refund processed. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP08-06** | White-Box (Attack) | User uploads malicious executable disguised as PDF (`exploit.exe.pdf`) into evidence dossier. | MIME magic bytes inspection detects binary PE header; rejects file with HTTP 415 Unsupported Media Type. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP08-07** | White-Box (Condition) | Arbitrator ruling with split percentages that do not sum to 100% (e.g., 60% client + 50% consultant = 110%). | Validation guard `sum_splits == 100.00` raises `InvalidSplitAllocationError`. Ruling cannot be submitted. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP08-08** | White-Box (Mutation) | Arbitrator role check: Non-arbitrator user attempts to submit adjudication ruling. | RBAC middleware checks caller role; raises HTTP 403 Forbidden. | _Pending — not yet executed_ | **NOT RUN** |

---

## Pass / Fail Summary
- **Execution status:** NOT RUN. This plan has been designed but not yet executed.
- **Observed results:** to be recorded only from actual execution, with a link to the test run / CI job as evidence.
- **Coverage:** to be measured with `pytest --cov` when executed. No coverage figure has been measured yet.

> [!NOTE]
> An earlier version of this file showed observed results and coverage figures that were never measured. They were removed on 13 Oct 2026 (CR-2026-002).
