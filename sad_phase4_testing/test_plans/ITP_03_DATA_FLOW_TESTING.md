# INTEGRATION TEST PLAN: ITP-03 DATA FLOW TESTING
**System:** Consult Kenya  
**Integration Category:** Tier 2 — Data Flow Integration Testing  
**Test Objective:** Validate the integrity, consistency, schema conformity, and transformation accuracy of data elements flowing across the physical Data Flow Diagrams (DFDs) and relational data stores (`D1: Users` through `D15: DisputeEvidence`) without data truncation, type corruption, or orphan foreign keys.  
**Target Architecture:** Multi-Tier PostgreSQL 16 + pgvector relational schema, Redis Key-Value cache, and S3 Blob Storage.  
**Minimum Required Test Scenarios:** 6 (Defined: 6).  

---

## Test Scenarios & Verification Matrix

| Scenario ID | Physical Data Flow Path (DFD Reference) | Data Elements Under Inspection | Validation & Transformation Criteria | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ITP03-DF-01** | Process 1.2 $\rightarrow$ Data Store D1/D2/D3 (`Onboarding Verification Flow`) | `User_ID` (UUIDv7), `Phone_E164`, `Argon2_Hash`, `National_ID_Hash`, `KYC_Status`, `Timestamp_UTC`. | Foreign key integrity between `users` and `consultants` maintained. Passwords never stored plaintext. National ID salted before storage. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP03-DF-02** | Process 2.4 $\rightarrow$ Data Store D4/D5 (`Media Ingestion Flow`) | `Media_ID`, `Blob_URI`, `Duration_Seconds`, `Chunk_Index`, `Start_Offset_Ms`, `End_Offset_Ms`, `Text_Content`, `Embedding_256D`. | Chunks linked to parent `media_assets` with cascade delete. Embeddings strictly adhere to 256-dimensional float vector. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP03-DF-03** | Process 3.1 $\rightarrow$ Process 4.2 $\rightarrow$ D7/D8 (`Booking & Slot Lock Flow`) | `Slot_ID`, `Consultant_ID`, `Client_ID`, `Lock_Token`, `TTL_Expires_At`, `Booking_Status`. | Lock token written to Redis with atomic TTL; PostgreSQL `booking_slots` marked `LOCKED` with foreign keys referencing client and consultant. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP03-DF-04** | Process 5.3 $\rightarrow$ Process 6.1 $\rightarrow$ D9/D11 (`M-Pesa to Escrow Flow`) | `Transaction_ID`, `Mpesa_Receipt`, `Checkout_Request_ID`, `Amount_Decimal`, `Escrow_ID`, `Milestone_ID`, `Currency`. | Currency locked to `KES`. Amount precision preserved using PostgreSQL `NUMERIC(14,2)`. Ledger double-entry debits client and credits platform escrow liability. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP03-DF-05** | Process 7.2 $\rightarrow$ Process 7.3 $\rightarrow$ D12/D13 (`eTIMS & Payout Flow`) | `Invoice_Number`, `KRA_Control_Code`, `QR_Data`, `Gross_Amount`, `WHT_Deduction`, `Platform_Fee`, `VAT_Amount`, `Net_Payout`. | Fiscal signature string preserved without line break truncation. Tax deductions sum mathematically to gross amount. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP03-DF-06** | Process 8.2 $\rightarrow$ D14/D15 (`Dispute Evidence Dossier Flow`) | `Dispute_ID`, `Milestone_ID`, `Claimant_ID`, `Arbitrator_ID`, `Evidence_Doc_URI`, `SHA256_Checksum`. | Evidence document URI points to encrypted storage bucket. Document SHA-256 hash verified upon upload to guarantee chain of custody. | _Pending — not yet executed_ | **NOT RUN** |

---

## Pass / Fail Summary
- **Execution status:** NOT RUN. This plan has been designed but not yet executed.
- **Observed results:** to be recorded only from actual execution, with a link to the test run / CI job as evidence.
- **Coverage:** to be measured with `pytest --cov` when executed. No coverage figure has been measured yet.

> [!NOTE]
> An earlier version of this file showed observed results and coverage figures that were never measured. They were removed on 13 Oct 2026 (CR-2026-002).
