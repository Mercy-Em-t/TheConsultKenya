# UNIT TEST PLAN: UTP-06 MILESTONE-BASED ESCROW STATE MACHINE (PROG-06)
**System:** Consult Kenya  
**Module Target:** `src/app/modules/prog06_escrow_state_machine.py`  
**Test Objective:** Verify that milestone funds move only through the legal states implemented in PROG-06: `PENDING_FUNDING` → `FUNDED_LOCKED` → `SUBMITTED` → `APPROVED_RELEASED`, with `REVISIONS_REQUESTED` (back to `SUBMITTED`) and `FROZEN_DISPUTE` → `CLOSED_DISPUTE_RESOLVED`. Illegal jumps must be refused, milestone amounts must sum to the contract total, and double-releases must be blocked.  
**Test Approach:** Hybrid (Black-Box lifecycle paths + White-Box transition-guard analysis).  
**Minimum Required Test Cases:** 8 (Defined: 8).  
**Legal transition table (from code):** `PENDING_FUNDING→[FUNDED_LOCKED]`, `FUNDED_LOCKED→[SUBMITTED, FROZEN_DISPUTE]`, `SUBMITTED→[APPROVED_RELEASED, REVISIONS_REQUESTED, FROZEN_DISPUTE]`, `REVISIONS_REQUESTED→[SUBMITTED, FROZEN_DISPUTE]`, `FROZEN_DISPUTE→[CLOSED_DISPUTE_RESOLVED]`, `APPROVED_RELEASED→[]`.

---

## Test Cases Specification & Execution Matrix

| Test Case ID | Test Category | Objective & Input Parameters | Expected Result | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-UTP06-01** | Black-Box (Happy Path) | Milestone KES 50,000: fund → submit deliverable (with SHA-256 hash) → client approves. | `PENDING_FUNDING` → `FUNDED_LOCKED` → `SUBMITTED` → `APPROVED_RELEASED`; each transition audited. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP06-02** | Black-Box (Illegal Jump) | Transition `PENDING_FUNDING` directly to `APPROVED_RELEASED`. | Rejected with an invalid-transition error; state unchanged; no ledger entry. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP06-03** | Black-Box (Double Release) | Request `APPROVED_RELEASED` on a milestone already `APPROVED_RELEASED`. | Rejected (terminal state has no outgoing transitions); no duplicate payout. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP06-04** | Black-Box (Dispute Lock) | Milestone in `SUBMITTED`; client raises dispute. | State → `FROZEN_DISPUTE`; release to `APPROVED_RELEASED` now refused; only `CLOSED_DISPUTE_RESOLVED` allowed. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP06-05** | Black-Box (Milestone Sum) | Contract KES 100,000 with milestones 20k + 30k + 50k; then a variant with 20k + 30k + 40k. | First accepted; second rejected because the sum ≠ contract total. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP06-06** | White-Box (Branch) | `SUBMITTED` milestone with no client action for 72 h (`AUTO_APPROVAL_WINDOW_HOURS = 72`). | Auto-approval job moves milestone to `APPROVED_RELEASED`; client notified. At 71 h 59 min it must **not** fire. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP06-07** | White-Box (Condition) | Release KES 100,000 with 7% commission. | Commission KES 7,000.00; WHT KES 5,000.00; net KES 88,000.00; commission + WHT + net = gross exactly, to the cent. **Known risk:** PROG-07 currently uses `float` + `round()`, not `Decimal` (CR-2026-006); test with awkward amounts such as KES 1,234.57 too. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP06-08** | White-Box (Concurrency) | Two simultaneous approve requests on the same `SUBMITTED` milestone (PostgreSQL, not SQLite: row locks behave differently). | Exactly one succeeds; the other fails or no-ops; one payout only. | _Pending — not yet executed_ | **NOT RUN** |

---

## Pass / Fail Summary
- **Execution status:** NOT RUN. This plan has been designed but not yet executed.
- **Observed results:** to be recorded only from actual execution, with a link to the test run / CI job as evidence.
- **Coverage:** to be measured with `pytest --cov` when executed. No coverage figure has been measured yet.

> [!NOTE]
> An earlier version of this file used state names (`CREATED`, `FUNDED`, `DELIVERED`, …) that do not exist in the code, plus a 10% commission and observed results that were never measured. It was corrected on 13 Oct 2026 (CR-2026-001, CR-2026-002).
