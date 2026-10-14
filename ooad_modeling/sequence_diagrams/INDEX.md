# SEQUENCE DIAGRAMS MASTER INDEX & INTERACTION CATALOG
**System:** Consult Kenya (Enterprise Advisory & Authority Network)  
**Standard:** UML 2.5 Dynamic Interaction Modeling  
**Lifecycle Stage:** Object-Oriented Analysis & Design  
**Total Diagrams:** 22 High-Fidelity Sequence Models  

---

## 1. Traceability Matrix: Use Cases to UML Sequence Models

Every business use case defined in Phase 2 has a corresponding sequence diagram capturing participating lifelines, synchronous/asynchronous messages, execution occurrences, and alternate branches:

| Use Case ID | Sequence Diagram File Link | Core Lifelines Involved | Transactional Focus |
| :--- | :--- | :--- | :--- |
| **UC-01** | [`SQ_UC01`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC01_Discover_Content_via_Dual-Mode_Feeds.md) | Client, FeedUI, VectorEngine, PostgreSQL, Redis | Dual-mode feed discovery & top-20 card ranking |
| **UC-02** | [`SQ_UC02`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC02_Inspect_Consultant_Portfolio_Bento_Grid.md) | Client, BentoGridUI, ProfileCtrl, Consultant | Dynamic Bento Grid assembly & verified badges |
| **UC-03** | [`SQ_UC03`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC03_Search_and_Filter_Topic_Hubs.md) | Client, SearchHubUI, FilterCtrl, DB | Multi-facet taxonomy filtering & price bounds |
| **UC-04** | [`SQ_UC04`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC04_Bookmark_and_Organize_Case_Studies.md) | Client, CaseStudyView, BookmarkCtrl, DB | Organizing saved authority briefs into collections |
| **UC-05** | [`SQ_UC05`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC05_Compose_Case_Study_Deck_via_Creation_Studio.md) | Consultant, StudioUI, StudioParser, DB | Real-time Markdown & Mermaid vector SVG compiling |
| **UC-06** | [`SQ_UC06`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC06_Tag_Evidence_and_Proof_of_Execution.md) | Consultant, EvidenceUI, S3 KMS Vault, DB | Cryptographic SHA-256 fingerprinting & proof upload |
| **UC-07** | [`SQ_UC07`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC07_Attach_Conversion_Anchor_Call-to-Action.md) | Consultant, DeckSettingsUI, AnchorCtrl, DB | Attaching 1-click consultation booking CTAs |
| **UC-08** | [`SQ_UC08`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC08_Verify_Professional_Identity_and_Credentials.md) | Consultant, AuthCtrl, StatutoryRegistryAdapter, Celery | LSK/ICPAK/EBK license check & Tier 3 upgrade |
| **UC-09** | [`SQ_UC09`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC09_Book_In-App_Advisory_Consultation.md) | Client, BookingUI, SlotLockManager, Redis, DB | Atomic 900s Redis slot lock & collision detection |
| **UC-10** | [`SQ_UC10`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC10_Process_Payment_via_M-Pesa_STK_Push.md) | Client, CheckoutUI, DarajaCoordinator, Safaricom, Ledger | STK Push, 72h idempotency barrier & escrow deposit |
| **UC-11** | [`SQ_UC11`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC11_Process_Cross-Border_Card_Payment.md) | Client, CardModal, CardGateway, Stripe (3DS), Ledger | Diaspora 3D-Secure card tokenization & currency conversion |
| **UC-12** | [`SQ_UC12`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC12_Conduct_Secure_Live_Consultation.md) | Client, Consultant, LiveKit SFU, SessionCtrl | Encrypted WebRTC audio/video call execution |
| **UC-13** | [`SQ_UC13`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC13_Fund_Milestone_Escrow_Contract.md) | Client, EscrowUI, EscrowFSM, Safaricom Daraja, DB | Milestone escrow funding & status to `FUNDED_LOCKED` |
| **UC-14** | [`SQ_UC14`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC14_Submit_Project_Milestone_Deliverable.md) | Consultant, DeliverableUI, EscrowFSM, S3 Vault, DB | Milestone deliverable hash & 72h clock trigger |
| **UC-15** | [`SQ_UC15`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC15_Review_and_Approve_Escrow_Milestone.md) | Client, EscrowFSM, TaxEngine, KRA eTIMS, Daraja B2C | Client sign-off, eTIMS invoice, 7% fee, 5% WHT, B2C payout |
| **UC-16** | [`SQ_UC16`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC16_Initiate_Escrow_Dispute_and_Mediation.md) | Client, DisputeModal, DisputeCtrl, EscrowFSM, DB | 7-day dispute window, funds frozen, 48h deadline |
| **UC-17** | [`SQ_UC17`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC17_Calculate_Creator_Authority_Score_(CAS).md) | HourlyCron, CASEngine, PostgreSQL, Redis | Recalculating CAS 4-factor multipliers in batch |
| **UC-18** | [`SQ_UC18`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC18_Personalize_Two-Pass_Discovery_Feed.md) | Client, FeedView, TwoPassEngine, pgvector, Redis | Pass 1 cosine candidate pull + Pass 2 CAS rerank |
| **UC-19** | [`SQ_UC19`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC19_Manage_Phased_Rollout_and_Creator_Onboarding.md) | Admin, AdminUI, RolloutManager, SystemConfigDB | Regional geofence expansion & pilot exit verification |
| **UC-20** | [`SQ_UC20`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC20_Moderate_Platform_Content_and_Enforce_NDAs.md) | ComplianceOfficer, ModerationUI, ModService, DB | Redacting sensitive corporate trademarks & client NDA |
| **UC-21** | [`SQ_UC21`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC21_Adjudicate_Milestone_Dispute.md) | Arbitrator, ArbitratorUI, DisputeEngine, Daraja B2C | Binding award split calculation (e.g. 60/40) & refund |
| **UC-22** | [`SQ_UC22`](file:///c:/Users/user/Documents/KenyaConsult/ooad_modeling/sequence_diagrams/SQ_UC22_Audit_Financial_Settlement_and_Tax_Compliance.md) | TaxAuditor, AuditPortal, AuditService, KRA eTIMS | Monthly KRA W2 & VAT-3 return reconciliation |
