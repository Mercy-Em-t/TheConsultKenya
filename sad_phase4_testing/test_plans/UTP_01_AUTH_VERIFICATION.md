# UNIT TEST PLAN: UTP-01 AUTHENTICATION & IPRS VERIFICATION (PROG-01)
**System:** Consult Kenya  
**Module Target:** `src/app/modules/prog01_auth_verification.py`  
**Test Objective:** Verify that consultant onboarding, password hashing, JWT token lifecycle, role-based access control (RBAC), and IPRS National ID verification function with mathematical correctness, zero security leaks, and resilient handling of valid, boundary, and malformed inputs.  
**Test Approach:** Hybrid (Black-Box Equivalence Partitioning + White-Box Statement & Branch Coverage).  
**Minimum Required Test Cases:** 8 (Defined: 8).  

---

## Test Cases Specification & Execution Matrix

| Test Case ID | Test Category | Objective & Input Parameters | Expected Result | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-UTP01-01** | Black-Box (Valid) | Valid Kenyan phone (`+254712345678`), valid password (`P@ssw0rd2026!`), valid National ID (`12345678`), Role: `CONSULTANT`. | HTTP 201 Created. User registered, password salted with Argon2id, JWT bearer token issued with 15-min expiration. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP01-02** | Black-Box (Malformed) | Nonsense phone number (`"not-a-number"` and `"+254000000000"`), password (`"short"`). | HTTP 422 Unprocessable Entity. Specific validation message indicating E.164 Kenyan mobile format and password entropy rule. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP01-03** | Black-Box (Boundary) | Password exactly 8 characters (Min allowed boundary) vs 7 characters (Sub-boundary reject). | 8 chars: Accepted (201). 7 chars: Rejected with HTTP 422 ("Password must be at least 8 characters"). | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP01-04** | Black-Box (Attack/Nonsense) | SQL injection payload in ID field: `' OR 1=1; DROP TABLE users; --` | Sanitized by Pydantic regex pattern `^[0-9]{7,9}$`. HTTP 422 validation failure. Zero SQL executed. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP01-05** | White-Box (Branch) | IPRS Mock Service returns `status: "DECEASED"` or `status: "MISMATCH"`. | Internal branch executes exception `IPRSIdentityMismatchError`. Status set to `REJECTED`, audit event logged in `VerificationAudit`. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP01-06** | White-Box (Path) | Token expiration path: Submit expired JWT token to protected endpoint `/api/v1/consultant/profile`. | Token verification branch catches `jwt.ExpiredSignatureError`, revokes session, returns HTTP 401 with `WWW-Authenticate: Bearer error="token_expired"`. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP01-07** | White-Box (Condition) | RBAC authorization matrix: User with role `CLIENT` attempts to invoke consultant-only endpoint `/api/v1/consultant/set-rates`. | RBAC check `require_role(["CONSULTANT"])` evaluates false; raises `HTTPException(status_code=403, detail="Forbidden: Insufficient privileges")`. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP01-08** | White-Box (Mutation) | Test stub failure: IPRS external gateway timeout (5000ms latency simulation). | System fails gracefully into retry loop, catches `GatewayTimeoutException`, returns HTTP 504 with retry-after header without crashing daemon. | _Pending — not yet executed_ | **NOT RUN** |

---

## Pass / Fail Summary
- **Execution status:** NOT RUN. This plan has been designed but not yet executed.
- **Observed results:** to be recorded only from actual execution, with a link to the test run / CI job as evidence.
- **Coverage:** to be measured with `pytest --cov` when executed. No coverage figure has been measured yet.

> [!NOTE]
> An earlier version of this file showed observed results and coverage figures that were never measured. They were removed on 13 Oct 2026 (CR-2026-002).
