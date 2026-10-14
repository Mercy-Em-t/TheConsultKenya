# UNIT TEST PLAN: UTP-04 DISTRIBUTED SLOT LOCK MANAGER (PROG-04)
**System:** Consult Kenya  
**Module Target:** `src/app/modules/prog04_slot_lock_manager.py`  
**Test Objective:** Verify that distributed calendar slot locks are acquired atomically with strict TTL (900 seconds), race conditions between concurrent clients booking the same consultant slot are resolved with zero double-bookings, and expired locks release automatically.  
**Test Approach:** Hybrid (Black-Box Concurrency Contention + White-Box Redis TTL / Mutex Expiry Branches).  
**Minimum Required Test Cases:** 8 (Defined: 8).  

---

## Test Cases Specification & Execution Matrix

| Test Case ID | Test Category | Objective & Input Parameters | Expected Result | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-UTP04-01** | Black-Box (Valid) | Single client requests lock on available slot `2026-11-01 10:00 EAT` for Consultant `C-101`. | HTTP 200 OK. Lock acquired. Returns lock token UUID, TTL countdown = 900s, slot status marked `LOCKED`. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP04-02** | Black-Box (Contention Race) | Two clients (`Client-A` and `Client-B`) attempt to acquire lock on the exact same slot within 5 milliseconds. | Exactly one client (`Client-A`) receives HTTP 200 with lock token. Other client (`Client-B`) receives HTTP 409 Conflict ("Slot is currently reserved by another client"). | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP04-03** | Black-Box (Boundary) | Lock refresh/extension request at 899 seconds (1s prior to expiration). | Allowed. TTL safely reset to 900s. Lock ownership verified against caller's token UUID. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP04-04** | Black-Box (Expired) | Client attempts to confirm booking after TTL has expired (901 seconds elapsed). | System detects lock expiration. Rejects confirmation with HTTP 410 Gone ("Slot lock expired. Please select a new slot"). | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP04-05** | White-Box (Branch) | Release lock: Authorized client cancels before expiration using correct lock token. | Lock removed immediately from Redis key space. Slot status reverts to `AVAILABLE`. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP04-06** | White-Box (Attack) | Malicious client attempts to release someone else's slot lock using fraudulent token. | Token comparison `caller_token == stored_token` evaluates false. Raises `UnauthorizedLockReleaseError`. Returns HTTP 403. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP04-07** | White-Box (Path) | Slot in past: Attempt to lock slot with timestamp `now() - 1 hour`. | Temporal validation branch catches past timestamp. Returns HTTP 422 ("Cannot book retrospective consultation slot"). | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP04-08** | White-Box (Mutation) | Redis node failover simulation: Redis returns `ConnectionError`. | Graceful fallback to PostgreSQL row-level locking (`SELECT FOR UPDATE NOWAIT`). Preserves transactional atomicity. | _Pending — not yet executed_ | **NOT RUN** |

---

## Pass / Fail Summary
- **Execution status:** NOT RUN. This plan has been designed but not yet executed.
- **Observed results:** to be recorded only from actual execution, with a link to the test run / CI job as evidence.
- **Coverage:** to be measured with `pytest --cov` when executed. No coverage figure has been measured yet.

> [!NOTE]
> An earlier version of this file showed observed results and coverage figures that were never measured. They were removed on 13 Oct 2026 (CR-2026-002).
