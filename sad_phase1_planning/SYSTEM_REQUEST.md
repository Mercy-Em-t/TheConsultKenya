# SYSTEM REQUEST: Consult Kenya Platform
**Document Identifier:** SR-2026-CK-001  
**Project Name:** Consult Kenya (Visual-First Professional Advisory & Authority Network)  
**Lifecycle Stage:** Systems Analysis & Design (SAD) — Phase 1: Project Identification & Initiation  
**Date Submitted:** October 12, 2026  
**Status:** Formally Submitted for Executive & Steering Committee Review  

---

## 1. Project Sponsor & Governance
* **Executive Project Sponsor:** Mercy & Leah (Founding Partners & Technical Architects, Flagship Consulting Practice).
* **Business Unit:** Systems Architecture, Enterprise Legal & Strategy Practice / Digital Marketplace Group.
* **Project Manager / Lead Analyst:** Antigravity (Chief Systems Analyst & Architect).
* **Steering Committee Representatives:**
  * Lead Technical Architect & Codebase IP Owner (Mercy)
  * Head of Practice Operations & Client Engagements (Leah)
  * External Legal Counsel & CIArb Accredited Mediator
  * Enterprise Client Advisory Representative

---

## 2. Business Need
In the East African commercial ecosystem (anchored in Nairobi, Kenya), high-value professional advisory services (software architecture, cloud security, corporate law, tax strategy) suffer from severe market failure caused by two opposing digital extremes:

1. **The Inadequacy of Legacy Professional Networks (The "Resume Blindness" Problem):**  
   Traditional platforms like LinkedIn rely on text-heavy resumes, static job titles, and unvetted self-endorsements. In our empirical problem discovery study ($N=30$), **86.7% of enterprise decision-makers and founders rated text resumes as providing near-zero signal** for actual technical delivery competence. Technical competence cannot be communicated through generic bullet points; enterprise buyers demand scannable visual proof of past execution (*Challenge $\to$ Solution $\to$ Impact*).

2. **The Superficiality of Consumer Social Networks (The "Fluff & Distraction" Problem):**  
   Platforms like Instagram and TikTok possess modern, high-engagement visual mechanics (swipeable carousels, short-form video loops, frictionless feeds) but completely lack the professional depth, verified statutory credentials, and transactional infrastructure required for high-stakes B2B advisory contracts.

3. **Transactional Drag & Mutual B2B Distrust (The "Payment & Dispute" Barrier):**  
   Independent specialists lose an average of **6.5 unbillable hours per month** in unpaid "informal discovery coffee" chats and manual payment chasing. Simultaneously, enterprise buyers and founders are terrified of paying upfront deposits to independent contractors who may deliver broken code and vanish (**93.3% of stakeholders reported past payment or scope deadlocks**). Furthermore, cross-border payments incur heavy wire friction, and domestic transactions require compliance with strict **Kenya Revenue Authority (KRA) eTIMS electronic tax invoicing mandates**.

**Core Business Driver:**  
To build an overarching digital ecosystem—**Consult Kenya**—that fuses the **high-engagement visual carousel and vertical stream mechanics of Instagram** with the **verified authority, statutory rigor, and commercial contracting utility of an enterprise advisory marketplace**.

---

## 3. Business Requirements (High-Level Capabilities)
The proposed system must provide the following core operational capabilities:

1. **Dual-Mode Ergonomic Interface (`CARD-004`, `CARD-005`):**
   * *Vertical Discovery Stream (Home)*: Immersive, full-screen vertical feed delivering swipeable case studies and 30–60s micro-videos with adaptive low-bandwidth streaming for mobile networks.
   * *Bento-Box Inspection Grid (Profile & Hubs)*: High-density modular grid enabling enterprise buyers to audit a consultant's authority baseline, statutory badges, and code commits in $\le 5\text{ seconds}$.
2. **Standardized Creation Studio (`CARD-006`):**
   * Eliminates "blank-page syndrome" via structured narrative templates (*Template A: Case Study*, *Template B: Explainer*, *Template C: Toolkit*) with a strict 300-character-per-slide anti-clutter limit and desktop split-screen preview.
3. **Verifiable Proof & Trust Layer (`CARD-003`, `CARD-008`):**
   * Automated verification hooks into the Kenyan National Identity gateway (IPRS), KRA PIN registry, and statutory boards (Law Society of Kenya, ICPAK, Engineers Board of Kenya).
   * Verified GitHub commit proof attachments and irreversible in-studio client IP redaction tools.
4. **Algorithmic Meritocracy (Authority Engine) (`CARD-007`):**
   * A multi-objective ranking algorithm governed by a **Creator Authority Score (CAS)** that weights verified statutory credentials ($40\%$) and completed contracts ($30\%$), while valuing private saves/bookmarks $5\times$ over superficial likes to suppress viral fluff.
   * A **Two-Pass AI Retrieval Engine** combining 128-dimensional dense vector embeddings with regional East African relevance weighting.
5. **Zero-Redirect Native Scheduling & Fintech Rails (`CARD-009`):**
   * Native in-app slide-up booking sheet with distributed 10-minute mutex slot locking (eliminating Calendly drop-offs).
   * Automated mobile **Safaricom M-Pesa STK Push** checkout, manual Paybill fallbacks, and multi-currency international card rails (USD/EUR/GBP) with live Central Bank of Kenya (CBK) exchange rate locking.
6. **Milestone Escrow Vault & Mediation Engine (`CARD-010`):**
   * Dedicated trust ledger securing enterprise deposits upfront against an itemized Statement of Work (SOW).
   * Cryptographic SHA-256 proof of delivery timestamping, a 72-hour client inspection window, a 7-day auto-approval fallback, and binding dispute mediation with optional CIArb Kenya arbitration referral.
   * Automated deduction of a **5% to 8% platform take rate** and real-time generation of **KRA eTIMS QR-coded tax invoices**.

---

## 4. Business Value (Expected Organizational Impact)

### Tangible Economic Benefits:
* **Direct Marketplace GMV & Platform Retention:**
  * By Phase 3 steady-state, processing an estimated 1,000 monthly transactions at an average advisory/milestone contract size of KES 25,000 generates KES 25,000,000 in monthly Gross Merchandise Volume (GMV).
  * A 7% average platform take rate captures **KES 1,750,000 in monthly net platform revenue** (KES 21,000,000 annually).
* **Flagship Agency Inbound Funnel (Phase 1):**
  * Serves as the high-converting inbound client engine for the founding consulting practice, capturing enterprise systems architecture and legal compliance retainers (projected KES 1,000,000+ monthly Billings in Phase 1 alone).
* **Reduction in Sales & Lead Acquisition Costs:**
  * Reduces client acquisition cost (CAC) for independent consultants by an estimated 65% by replacing unbillable manual pitching with automated visual authority distribution.

### Intangible Strategic Benefits:
* **Brand Authority & Category Creation:**
  * Establishes "Consult Kenya" as the definitive national and regional digital authority directory for vetted professional talent across East Africa.
* **Elimination of Bad-Faith Transaction Risks:**
  * Protects both corporate buyers and independent practitioners from financial fraud, non-delivery, and payment abandonment via automated escrow guarantees.
* **Statutory Compliance Leadership:**
  * Full native alignment with the Kenya Data Protection Act (DPA 2019) and KRA eTIMS electronic fiscal regulations, positioning the platform as an enterprise-grade institutional partner.

---

## 5. Special Issues, Constraints & Strategic Timing

1. **Strategic Rollout Gating (The 3-Phase Flywheel) (`CARD-002`):**
   * To solve the marketplace "chicken-and-egg" cold start, the system *must not* launch as an open free-for-all marketplace.
   * **Phase 1 (Anchor Agency):** 100% of published case studies originate from the proprietary founding consultancy to establish the aesthetic standard and prove unit economics.
   * **Phase 2 (Curated Cohort):** Access is unlocked via cryptographic invitation codes for 25 hand-picked specialist peers.
   * **Phase 3 (Open Ecosystem):** Self-service vetted onboarding opens with multi-tenant SaaS profile tiers.
2. **Fintech Merchant of Record Regulatory Boundaries:**
   * The platform must partner with licensed Central Bank of Kenya (CBK) Payment Service Providers (Paystack / Flutterwave / Safaricom Daraja) as Merchant of Record to avoid unlicensed deposit-taking classifications.
3. **Intellectual Property Protection:**
   * Enterprise trade secrets must be protected via an emergency **4-hour SLA takedown workflow** and in-studio client redaction tools.
4. **Target Completion Window:**
   * Phase 1 core architecture and pilot launch within 8–12 weeks of initiation.

---

## 6. Formal Sign-Off & Recommendation

| Role | Reviewer Name | Recommendation | Signature Status |
| :--- | :--- | :---: | :---: |
| **Executive Project Sponsor** | Lead Architecture Partner | **APPROVED FOR SAD LIFECYCLE** | Signed (Oct 12, 2026) |
| **Chief Systems Analyst** | Antigravity SAD Team | **PROCEED TO FEASIBILITY ANALYSIS** | Signed (Oct 12, 2026) |
| **Steering Committee Chair** | Practice Operations Lead | **APPROVED TO COMMIT RESOURCES** | Signed (Oct 12, 2026) |

---

> **Steering Committee Decision:**  
> The System Request for **Consult Kenya (SR-2026-CK-001)** is formally accepted. The systems analysis team is authorized to proceed immediately to **Feasibility Analysis** (Technical, Economic, Organizational/Operational).
