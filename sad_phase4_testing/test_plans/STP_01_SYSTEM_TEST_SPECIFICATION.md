# SYSTEM TEST PLAN: STP-01 SYSTEM TEST SPECIFICATION
**System:** Consult Kenya  
**Testing Category:** Tier 3 — System Testing (Non-Functional & End-to-End Functional Verification)  
**Test Objective:** Validate the complete, integrated Consult Kenya software platform against business requirements, usability heuristics, security standards (OWASP Top 10 & Kenya Data Protection Act 2019), and high-load performance benchmarks.  
**Scope:** Whole-system integration running on staging architecture (Multi-AZ ECS Fargate + RDS PostgreSQL 16 pgvector + Redis ElastiCache + Cloudflare Edge).  
**Minimum Required Test Specifications:** 10 (Defined: 10).  

---

## System Test Specifications & Verification Matrix

| Spec ID | System Test Dimension | Objective & Verification Procedure | Acceptance Criteria & Thresholds | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **STP-01** | **Business Requirements Compliance** | Verify that all functional requirements documented in Phase 2 Requirements Definition (FR-01 through FR-22) are implemented without omission. | 100% of functional requirements operational. Zero missing core features. | _Pending — not yet executed_ | **NOT RUN** |
| **STP-02** | **Usability & UX Benchmarking** | Evaluate navigation efficiency, content awareness, and cognitive load using 10 novice users in Nairobi. | User task completion rate $> 95\%$; Average time to book a consultant $< 3\text{ minutes}$; System Usability Scale (SUS) score $> 85/100$. | _Pending — not yet executed_ | **NOT RUN** |
| **STP-03** | **Security: OWASP Top 10 Injection & XSS** | Run automated security penetration scan (OWASP ZAP / Burp Suite) targeting all input fields, vector search endpoints, and URL params. | Zero High/Critical vulnerabilities. No SQLi, No Command Injection, No Stored/Reflected XSS. | _Pending — not yet executed_ | **NOT RUN** |
| **STP-04** | **Security: Data Privacy & KDPA 2019 Compliance** | Verify that personal data (Kenyan National ID, Phone number, Video transcripts, Billing details) is encrypted at rest (AES-256) and in transit (TLS 1.3). | Strict compliance with Office of the Data Protection Commissioner (ODPC) guidelines. Sensitive PII pseudonymized in logs. | _Pending — not yet executed_ | **NOT RUN** |
| **STP-05** | **Performance: Vector Search Latency** | Benchmark pgvector HNSW cosine similarity query latency with 50,000 consultant profile embeddings in PostgreSQL database. | 95th percentile latency ($P_{95}$) $< 50\text{ms}$; 99th percentile ($P_{99}$) $< 100\text{ms}$. | _Pending — not yet executed_ | **NOT RUN** |
| **STP-06** | **Performance: Concurrency & Stress Testing** | Simulate 1,000 simultaneous active users performing search, browsing profiles, and initiating slot locks via Locust load test. | System maintains throughput $\ge 300\text{ requests/sec}$; Error rate $< 0.1\%$; CPU utilization on Fargate $< 75\%$. | _Pending — not yet executed_ | **NOT RUN** |
| **STP-07** | **Escrow Financial Precision & ACID Audit** | Execute 500 simultaneous multi-milestone payments, partial refunds, and KRA eTIMS disbursements. | General ledger double-entry reconciliation strictly balances to KES 0.00 difference. Zero missing cents. | _Pending — not yet executed_ | **NOT RUN** |
| **STP-08** | **High Availability & Fault Tolerance** | Simulate immediate failure of primary PostgreSQL RDS instance (trigger Multi-AZ failover) during active sessions. | System automatically reconnects to standby replica in $< 45\text{ seconds}$; Zero persistent data corruption. | _Pending — not yet executed_ | **NOT RUN** |
| **STP-09** | **WebRTC Media Performance under Jitter** | Test LiveKit video consultation under degraded network conditions (Simulated Kenyan rural mobile: 15% packet loss, 300ms jitter, 1.2 Mbps bandwidth). | Dynamic bitrate adaptation engages; Audio remains intelligible; Session does not disconnect unexpectedly. | _Pending — not yet executed_ | **NOT RUN** |
| **STP-10** | **Disaster Recovery & Backup Restoration** | Execute automated point-in-time recovery (PITR) of database from automated S3 WAL archive. | Recovery Point Objective (RPO) $< 5\text{ minutes}$; Recovery Time Objective (RTO) $< 30\text{ minutes}$. | _Pending — not yet executed_ | **NOT RUN** |

---

## Pass / Fail Summary
- **Execution status:** NOT RUN. This plan has been designed but not yet executed.
- **Observed results:** to be recorded only from actual execution, with a link to the test run / CI job as evidence.
- **Coverage:** to be measured with `pytest --cov` when executed. No coverage figure has been measured yet.

> [!NOTE]
> An earlier version of this file showed observed results and coverage figures that were never measured. They were removed on 13 Oct 2026 (CR-2026-002).
