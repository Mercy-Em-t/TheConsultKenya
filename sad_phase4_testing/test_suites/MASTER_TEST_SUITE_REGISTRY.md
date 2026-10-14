# MASTER TEST SUITE REGISTRY & EXECUTION INDEX
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Lifecycle Stage:** Phase 4 — Implementation & Quality Assurance  
**Author:** Chief Test Architect & Quality Directorate  
**Date:** October 2026 (Updated: 13 Oct 2026 per CR-2026-001 & CR-2026-002)  
**Status:** SPECIFICATION COMPLETE — EXECUTION PENDING (GATE G0)  

---

## 1. Master Quality Dashboard & Test Execution Status

| Testing Tier | Total Test Plans | Total Discrete Cases / Scenarios Designed | Status | Executed | Pass Rate | Code Coverage Target |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Tier 1: Unit Testing (UTP)** | 8 Plans | 64 Cases | Pending G0 | 0 / 64 | Pending | $\ge 90\%$ (Money paths) |
| **Tier 2: Integration Testing (ITP)** | 4 Plans | 24 Scenarios | Pending G0 | 0 / 24 | Pending | 100% Contract Integrity |
| **Tier 3: System Testing (STP)** | 1 Plan | 10 Specifications | Pending G0 | 0 / 10 | Pending | OWASP Top-10 / KDPA 2019 |
| **Tier 4: Acceptance Testing (ATP)** | 1 Plan | 6 UAT Work Streams | Pending Pilot | 0 / 6 | Pending | Target NPS $> +65$ |
| **TOTAL DESIGNED** | **14 Plans** | **104 Cases / Scenarios** | **PENDING G0** | **0 / 104** | **Pending** | **Real CI Execution** |

> [!IMPORTANT]
> **Audit Notice (13 Oct 2026):** An earlier version of this dashboard reported simulated/fabricated results (104/104 passed). Under CR-2026-002, all statuses have been reset to **Pending**. Execution against real staging infrastructure, PostgreSQL 16, and actual sandbox environments is tracked at **Gate G0** prior to Phase 5 conversion.

---

## 2. Directory Index of Modular Test Plans

All test plans are stored in dedicated individual files under `sad_phase4_testing/test_plans/`:

### Tier 1: Unit Test Plans (PROG-01 through PROG-08)
1. [`UTP_01_AUTH_VERIFICATION.md`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase4_testing/test_plans/UTP_01_AUTH_VERIFICATION.md) — Consultant Onboarding, Password Hashing, JWT Lifecycle, IPRS Verification (8 cases: 4 Black-Box, 4 White-Box).
2. [`UTP_02_STUDIO_PARSER.md`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase4_testing/test_plans/UTP_02_STUDIO_PARSER.md) — Advisory Video/Audio Parser, Speech-to-Text Chunker, MIME and Duration Boundary Validation (8 cases).
3. [`UTP_03_VECTOR_ENGINE.md`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase4_testing/test_plans/UTP_03_VECTOR_ENGINE.md) — Two-Pass AI Vector Engine, pgvector HNSW Cosine Similarity, 256-dim Vectors, Reciprocal Rank Fusion (8 cases).
4. [`UTP_04_SLOT_LOCK_MANAGER.md`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase4_testing/test_plans/UTP_04_SLOT_LOCK_MANAGER.md) — Distributed Redis Slot Lock, 900s TTL Expiration, Concurrency Contention, Double-Booking Prevention (8 cases).
5. [`UTP_05_MPESA_DARAJA.md`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase4_testing/test_plans/UTP_05_MPESA_DARAJA.md) — Safaricom Daraja STK Push, Callback Webhooks, Duplicate Callback Idempotency, Cancellation/Timeout Handling (8 cases).
6. [`UTP_06_ESCROW_STATE_MACHINE.md`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase4_testing/test_plans/UTP_06_ESCROW_STATE_MACHINE.md) — Milestone Escrow FSM (`PENDING_FUNDING` $\to$ `FUNDED_LOCKED` $\to$ `SUBMITTED` $\to$ `APPROVED_RELEASED`), Illegal State Jump Prevention, Double-Release Protection, 7% Commission, 72h Auto-approval (8 cases).
7. [`UTP_07_KRA_ETIMS_PAYOUT.md`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase4_testing/test_plans/UTP_07_KRA_ETIMS_PAYOUT.md) — KRA eTIMS Fiscal Invoice Generation, 7% Fee, 5% WHT Deduction, 16% VAT Platform Fee, Safaricom B2C Payouts (8 cases).
8. [`UTP_08_DISPUTE_ADJUDICATION.md`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase4_testing/test_plans/UTP_08_DISPUTE_ADJUDICATION.md) — Dispute Case Intake, Evidence Dossier Validation, Arbitration Split Calculus, Default Judgments (8 cases).

### Tier 2: Integration Test Plans
9. [`ITP_01_USER_INTERFACE_TESTING.md`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase4_testing/test_plans/ITP_01_USER_INTERFACE_TESTING.md) — User Interface Integration (Search Ribbon, Slot Picker, M-Pesa Checkout Dialog, LiveKit Video Container, Keystroke scripts).
10. [`ITP_02_USE_SCENARIO_TESTING.md`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase4_testing/test_plans/ITP_02_USE_SCENARIO_TESTING.md) — Use Scenario Integration (Complete Advisory Engagement, Onboarding to First Booking, Retainer Milestones, Dispute Split).
11. [`ITP_03_DATA_FLOW_TESTING.md`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase4_testing/test_plans/ITP_03_DATA_FLOW_TESTING.md) — Data Flow Integration (DFD Processes to Data Stores D1 through D15, Schema Conformity, 256-dim Vector Lengths, General Ledger Debits/Credits).
12. [`ITP_04_SYSTEM_INTERFACE_TESTING.md`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase4_testing/test_plans/ITP_04_SYSTEM_INTERFACE_TESTING.md) — System Interface Integration (Safaricom Daraja APIv2, KRA eTIMS OSCU, LiveKit Cloud WebRTC SFU, IPRS Mock Gateway, Cloudflare CDN).

### Tier 3 & Tier 4: System & Acceptance Test Plans
13. [`STP_01_SYSTEM_TEST_SPECIFICATION.md`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase4_testing/test_plans/STP_01_SYSTEM_TEST_SPECIFICATION.md) — System Non-Functional & End-to-End Test (Business Requirements, Usability, OWASP Top 10 Security, KDPA 2019, 420 RPS Stress Test, Disaster Recovery).
14. [`ATP_01_USER_ACCEPTANCE_TESTING.md`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase4_testing/test_plans/ATP_01_USER_ACCEPTANCE_TESTING.md) — Alpha Testing (Legal Counsel, Finance Controller, CPO) & Beta Field Pilot (35 external participants across Nairobi, target NPS $> +65$).

---

## 3. Real Automated Test Execution Harness
The executable test suite consists of actual `pytest` tests executed against application modules:
```powershell
python -m pytest tests/unit/test_backend_modules.py -v
```
To run the automated suite and output real execution status, execute:
```powershell
python tests/run_all_tests.py
```
This script executes real unit checks via pytest, computes exact financial ledger balancing using actual configuration settings, and reports truthful execution metrics without hardcoded passes.
