# INTEGRATION TEST PLAN: ITP-02 USE SCENARIO TESTING
**System:** Consult Kenya  
**Integration Category:** Tier 2 — Use Scenario Integration Testing  
**Test Objective:** Validate that realistic, multi-step operational journeys traversing multiple users, roles, and asynchronous business processes execute end-to-end without breakdown, state inconsistencies, or orphaned data records.  
**Target Scenarios:** Derived from Phase 2 Dennis-Wixom Use Cases (UC-01 through UC-22) and Phase 3 Scenarios.  
**Minimum Required Test Scenarios:** 6 (Defined: 6).  

---

## Test Scenarios & Verification Matrix

| Scenario ID | Use Scenario Title & Persona Journey | Execution Sequence Across Subsystems | Expected Multi-Role Outcome | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ITP02-SC-01** | **Complete Advisory Engagement Journey** (Corporate SME Owner Wanjiku & Tax Consultant Dr. Omondi) | 1. Client searches for tax advisor.<br>2. Selects Dr. Omondi, locks 1-hour slot.<br>3. Completes M-Pesa escrow payment (KES 10,000).<br>4. Attends WebRTC advisory video consultation.<br>5. Dr. Omondi uploads written advisory summary.<br>6. Wanjiku approves deliverable.<br>7. System generates KRA eTIMS invoice, deducts WHT (KES 500) & 7% fee (KES 700, of which KES 112 is VAT), disburses net KES 8,800 to Dr. Omondi via M-Pesa B2C. | End-to-end transaction completes with zero human administrative intervention. Both parties receive notification and fiscal receipts. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP02-SC-02** | **Consultant Onboarding to First Verified Booking** (New Legal Advocate Mutua) | 1. Mutua registers with Kenyan National ID.<br>2. System validates National ID via IPRS.<br>3. Mutua uploads 3-minute video advisory brief on property conveyancing.<br>4. Media parser transcribes & vector engine embeds brief.<br>5. Mutua profile appears in search.<br>6. Prospective client discovers and books Mutua. | Profile transitions from `UNVERIFIED` to `VERIFIED_ACTIVE`. Video searchable within 3 minutes of upload. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP02-SC-03** | **Multi-Milestone Retainer Engagement** (Agricultural Cooperative & Agronomist) | 1. Project created with 3 milestones totaling KES 150,000.<br>2. Client deposits funds into milestone 1.<br>3. Milestone 1 delivered and approved; released to consultant.<br>4. Client funds milestone 2.<br>5. Milestone 2 deliverable rejected by client for revisions.<br>6. Consultant revises deliverable and re-submits.<br>7. Client approves revision. | Escrow balances track accurately per milestone. Rejection triggers revision workflow without losing escrow security. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP02-SC-04** | **Arbitration & Disputed Milestone Split** (Construction Consultant & Property Developer) | 1. Milestone delivered.<br>2. Developer lodges dispute claiming incomplete structural drawings.<br>3. Both parties upload evidence dossiers.<br>4. Arbitrator Kamau reviews dossier in console.<br>5. Arbitrator rules 50/50 split.<br>6. Platform disburses KES 25,000 refund to developer and KES 25,000 (net) to consultant. | Escrow unlocks precisely along ruling fractions. Case closed with signed arbitration award PDF. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP02-SC-05** | **Emergency Consultation Session Rescheduling** | 1. Client books slot for tomorrow 11:00 AM.<br>2. Consultant experiences emergency court appearance, requests reschedule 24h prior.<br>3. Client receives interactive SMS/Email to accept new slot or receive 100% refund.<br>4. Client accepts new slot. | Slot transferred to new timestamp with zero financial transaction penalty. Calendar invite refreshed. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP02-SC-06** | **High-Volume Search & Filter Concurrency** (50 Concurrent Clients in Nairobi) | 50 automated test clients perform simultaneous vector searches across legal, engineering, financial domains. | Engine maintains average response latency under 65ms with zero HTTP 500 errors. | _Pending — not yet executed_ | **NOT RUN** |

---

## Pass / Fail Summary
- **Execution status:** NOT RUN. This plan has been designed but not yet executed.
- **Observed results:** to be recorded only from actual execution, with a link to the test run / CI job as evidence.
- **Coverage:** to be measured with `pytest --cov` when executed. No coverage figure has been measured yet.

> [!NOTE]
> An earlier version of this file showed observed results and coverage figures that were never measured. They were removed on 13 Oct 2026 (CR-2026-002).
