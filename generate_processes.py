import os

processes_dir = r"c:\Users\user\Documents\KenyaConsult\processes"
os.makedirs(processes_dir, exist_ok=True)

# 1. Master processes list definitions
processes_list = [
    {
        "id": "PROC-1.0",
        "name": "Manage User Identity, Onboarding & Professional Verification",
        "owner": "Consultant / Client / Compliance Officer",
        "description": "Handles account registration, multi-factor authentication, profile creation, and statutory credential validation against Kenyan government and professional bodies (IPRS, KRA, LSK, ICPAK, EBK).",
        "external_entities": ["Client", "Consultant", "Platform Administrator", "Government & Professional Registries (IPRS, KRA, LSK, ICPAK, EBK)"],
        "data_stores": [
            "D1: User & Credential Registry",
            "D2: Compliance & Audit Vault",
            "D8: Configuration & Policy Datastore"
        ],
        "inputs": [
            ("Registration details & Credentials", "Client / Consultant"),
            ("National ID, KRA PIN, Board Registration # & License scan", "Consultant"),
            ("Verification responses & standing status", "Registries API"),
            ("Invite Codes & Cohort Policy", "Platform Administrator")
        ],
        "outputs": [
            ("Authentication Tokens & Session Profile", "Client / Consultant"),
            ("Verification Query Payload", "Registries API"),
            ("Verified Specialist Seal & Authority Tier Upgrade", "Consultant Profile / D1"),
            ("Compliance Audit Log Record", "D2: Compliance & Audit Vault")
        ],
        "subprocesses": [
            ("1.1", "Register & Authenticate User", "Validates user contact info, issues OTP/MFA, and establishes session."),
            ("1.2", "Curate Profile & Bento Grid Architecture", "Structures bio, skill tags, case study previews, and fee schedules."),
            ("1.3", "Ingest & Sanitize Professional Credentials", "Extracts metadata from licenses and scrubs PII from public view."),
            ("1.4", "Verify Credentials via External Registries", "Executes automated checks against IPRS, KRA, and professional board APIs."),
            ("1.5", "Manage Cohort Onboarding & Invite Codes", "Enforces rollout gates (Anchor Agency -> Curated Beta -> Open Ecosystem).")
        ]
    },
    {
        "id": "PROC-2.0",
        "name": "Author, Audit & Publish Visual Case Studies",
        "owner": "Consultant / Compliance Officer / Moderation Daemon",
        "description": "Governs the authoring lifecycle of structured case studies in Creation Studio, rendering Mermaid SVG diagrams, attaching cryptographic execution proofs, configuring conversion CTAs, and automated Data Loss Prevention (DLP) moderation.",
        "external_entities": ["Consultant", "Compliance Officer", "External Code Repositories (GitHub/GitLab)"],
        "data_stores": [
            "D3: Case Studies & Artifacts Datastore",
            "D4: Evidence & Execution Proofs Vault",
            "D2: Compliance & Audit Vault"
        ],
        "inputs": [
            ("Modular narrative markdown & metrics", "Consultant"),
            ("Mermaid architecture syntax & code blocks", "Consultant"),
            ("Proof URLs, commit hashes, audit PDFs", "Consultant"),
            ("Commit verification payloads", "GitHub / GitLab API"),
            ("Moderation & Redaction directives", "Compliance Officer")
        ],
        "outputs": [
            ("Live Rendered SVG Diagrams & Split-Screen Preview", "Consultant Display"),
            ("SHA-256 Proof Fingerprint & Verified Badges", "D4 / Case Study"),
            ("Sanitized Published Case Study Deck", "D3: Case Studies Datastore"),
            ("DLP Security Alert & Moderation Dossier", "Compliance Officer / D2")
        ],
        "subprocesses": [
            ("2.1", "Draft Modular Case Study Sections", "Parses Problem, Architecture Blueprint, Implementation, and Quantified Impact."),
            ("2.2", "Compile Architecture Diagrams & Code Blocks", "Generates real-time interactive SVG renderings from textual Mermaid syntax."),
            ("2.3", "Verify & Digest Execution Proofs", "Validates external repo commits and computes immutable SHA-256 digests."),
            ("2.4", "Bind Native Conversion Anchor CTA", "Configures embedded booking drawers and advisory fee structures."),
            ("2.5", "Scan for DLP Confidentiality & Redact IP", "Applies regex scanners for credentials and sensitive client trade secrets.")
        ]
    },
    {
        "id": "PROC-3.0",
        "name": "Discover, Search & Personalize Content Delivery",
        "owner": "Client / AI Recommendation Daemon",
        "description": "Retrieves and delivers hyper-relevant case studies and specialist profiles via a Two-Pass algorithmic engine combining pgvector semantic search, Creator Authority Scores (CAS), and regional East African weights.",
        "external_entities": ["Client", "Guest Visitor"],
        "data_stores": [
            "D3: Case Studies & Artifacts Datastore",
            "D5: Creator Authority & Telemetry Cache (Redis)",
            "D7: User Collections & Bookmarks DB"
        ],
        "inputs": [
            ("Feed request & display preference (Vertical vs. Grid)", "Client"),
            ("Natural language search query & facet filters", "Client"),
            ("Dwell time & interaction telemetry", "Client Device"),
            ("Bookmark & Collection save requests", "Client")
        ],
        "outputs": [
            ("Two-Pass Ranked Discovery Feed Payload", "Client Display"),
            ("Segmented Search Results (Decks, Experts, Tags)", "Client Display"),
            ("Personalized Collection Index", "Client Display / D7"),
            ("5x Engagement Multiplier Signal", "D5: Telemetry Cache")
        ],
        "subprocesses": [
            ("3.1", "Ingest Client Session Context & Geo-Intent", "Captures client domain history and regional location data."),
            ("3.2", "Execute Pass-1 ANN Vector Retrieval", "Performs high-speed approximate nearest neighbor search across embeddings."),
            ("3.3", "Execute Pass-2 CAS & Diversity Re-Ranking", "Applies business weights (CAS, freshness, geo) and author diversity limits."),
            ("3.4", "Deliver Dual-Mode Feed Stream", "Serves pre-buffered responsive cards with low-bandwidth fallbacks."),
            ("3.5", "Process Semantic Search & Facet Filters", "Executes hybrid vector + full-text filtering across topic hubs."),
            ("3.6", "Manage Bookmarks & Organize Collections", "Stores curated decks in client folders and emits algorithmic boosts.")
        ]
    },
    {
        "id": "PROC-4.0",
        "name": "Schedule & Conduct Live Advisory Consultations",
        "owner": "Client / Consultant / Video Engine",
        "description": "Orchestrates direct calendar slot reservation, 15-minute temporary coordination locks, intake question capture, and zero-friction WebRTC video conference delivery.",
        "external_entities": ["Client", "Consultant", "External Calendar Services (Google/Outlook)", "WebRTC Video Media Server"],
        "data_stores": [
            "D1: User & Credential Registry",
            "D6: Bookings & Consultation Datastore",
            "D10: Active Slot Locks & Coordination Cache"
        ],
        "inputs": [
            ("Availability calendar query & slot selection", "Client"),
            ("External calendar busy/free blocks", "Calendar Services API"),
            ("Pre-consultation briefing responses & files", "Client"),
            ("WebRTC media streams & shared notes", "Client & Consultant"),
            ("Session termination signal", "Client / Consultant")
        ],
        "outputs": [
            ("15-Minute Slot Lock Reservation", "D10: Active Slot Locks"),
            ("Pending Booking Record & Fee Invoice", "D6: Bookings DB"),
            ("Confirmed Calendar Invites with Room Tokens", "Client, Consultant & Calendar API"),
            ("Encrypted Peer-to-Peer A/V Session", "Client & Consultant"),
            ("Session Duration Telemetry & Summary PDF", "D6 / Participant Email")
        ],
        "subprocesses": [
            ("4.1", "Synchronize Real-Time Calendar Availability", "Queries external calendar providers to display unconflicted slots."),
            ("4.2", "Coordinate Slot Soft-Locking & Intake Capture", "Enforces 15-minute Redis reservation while collecting client briefs."),
            ("4.3", "Finalize Booking & Generate Meeting Access Tokens", "Binds confirmed payment to cryptographic WebRTC room tokens."),
            ("4.4", "Establish Encrypted WebRTC Live Session", "Coordinates DTLS-SRTP peer media streaming and shared scratchpad."),
            ("4.5", "Monitor Session Telemetry & Handle No-Shows", "Logs call duration and executes automated no-show policy.")
        ]
    },
    {
        "id": "PROC-5.0",
        "name": "Process Multi-Rail Payments & Escrow Ledger Accounting",
        "owner": "Client / Consultant / Safaricom Daraja / Bank Gateway",
        "description": "Executes payments via Safaricom M-Pesa STK Push, international 3D Secure cards, and RTGS wire transfers; locks funds into trust escrow; and manages double-entry ledger settlement.",
        "external_entities": ["Client", "Consultant", "Safaricom M-Pesa Daraja Gateway", "Card Payment Processor (Paystack/Flutterwave)", "Commercial Settlement Bank"],
        "data_stores": [
            "D6: Bookings & Consultation Datastore",
            "D9: Immutable Escrow & Financial Ledger",
            "D2: Compliance & Audit Vault"
        ],
        "inputs": [
            ("M-Pesa phone number & Payment initiation", "Client"),
            ("Daraja STK push callback payload", "Safaricom Gateway"),
            ("Tokenized card data & 3DS confirmation", "Client / Card Processor"),
            ("RTGS wire settlement notification", "Commercial Settlement Bank")
        ],
        "outputs": [
            ("Daraja STK Push Request", "Safaricom Daraja API"),
            ("Card Charge & 3DS Challenge", "Card Processor API"),
            ("Double-Entry Escrow Lock Entry", "D9: Escrow Ledger"),
            ("Payment Confirmation & Escrow Receipt", "Client & Consultant"),
            ("Escrow State Update ('CONFIRMED_ESCROW_LOCKED')", "D6: Bookings DB")
        ],
        "subprocesses": [
            ("5.1", "Initiate & Poll M-Pesa STK Push", "Dispatches Lipa Na M-Pesa USSD prompt and processes callback."),
            ("5.2", "Process Multi-Currency Card & 3DS Rails", "Tokenizes card credentials and handles CBK exchange rate conversions."),
            ("5.3", "Reconcile High-Value RTGS Bank Transfers", "Issues Virtual Account Numbers (VAN) and processes bank settlement webhooks."),
            ("5.4", "Maintain Double-Entry Escrow Ledger", "Records segregated trust balances under immutable contract UUIDs.")
        ]
    },
    {
        "id": "PROC-6.0",
        "name": "Manage Milestone SOW Contracts, Deliverables & Payouts",
        "owner": "Client / Consultant / KRA eTIMS / B2C Payout Rail",
        "description": "Governs multi-stage SOW consulting contracts, cryptographic delivery fingerprinting, 72-hour client inspection windows, contractual auto-approvals, KRA eTIMS tax compliance, and automated B2C consultant payouts.",
        "external_entities": ["Client", "Consultant", "Kenya Revenue Authority (KRA eTIMS API)", "M-Pesa B2C Payout Rail"],
        "data_stores": [
            "D3: Case Studies & Artifacts Datastore",
            "D9: Immutable Escrow & Financial Ledger",
            "D2: Compliance & Audit Vault",
            "D5: Creator Authority & Telemetry Cache"
        ],
        "inputs": [
            ("SOW Proposal & Milestone Definitions", "Consultant & Client"),
            ("Milestone Deliverable Files & GitHub PRs", "Consultant"),
            ("Milestone Approval + 2FA Confirmation", "Client"),
            ("72-Hour Inspection Countdown Timer Expiry", "System Clock"),
            ("Revision Feedback Notes", "Client")
        ],
        "outputs": [
            ("SHA-256 Deliverable Fingerprint & Delivery Timestamp", "D3 / D2"),
            ("Client Review Notification & Countdown Event", "Client"),
            ("Statutory KRA eTIMS Electronic Invoice with QR", "KRA API & Client"),
            ("Automated B2C Payout Instruction (Net after 7% take rate)", "M-Pesa B2C Rail"),
            ("Net Funds & Payout Confirmation", "Consultant"),
            ("Milestone State Update ('COMPLETED_RELEASED')", "D9: Escrow Ledger")
        ],
        "subprocesses": [
            ("6.1", "Initialize Milestone SOW Contract", "Binds contractual milestones to escrow funding tranches."),
            ("6.2", "Submit & Fingerprint Milestone Deliverable", "Computes SHA-256 checksums and begins 72-hour review clock."),
            ("6.3", "Process Client Milestone Review & Approval", "Captures client acceptance or revision requests."),
            ("6.4", "Enforce 72-Hour Contractual Auto-Approval", "Automatically clears undisputed deliverables upon timer lapse."),
            ("6.5", "Deduct Platform Take Rate & Generate eTIMS Invoice", "Calculates 7% commission and queries KRA electronic tax system."),
            ("6.6", "Disburse Net Payout via M-Pesa B2C Rails", "Transfers net remuneration directly to consultant's phone.")
        ]
    },
    {
        "id": "PROC-7.0",
        "name": "Adjudicate Escrow Disputes & Mediate Contracts",
        "owner": "Client / Consultant / Escrow Mediator",
        "description": "Freezes disputed escrow funds, aggregates legal dossiers, coordinates 48-hour rebuttal submissions, and facilitates binding mediator rulings with prorated payouts and legal certificates.",
        "external_entities": ["Client", "Consultant", "Escrow Mediator / Legal Auditor"],
        "data_stores": [
            "D9: Immutable Escrow & Financial Ledger",
            "D2: Compliance & Audit Vault",
            "D3: Case Studies & Artifacts Datastore"
        ],
        "inputs": [
            ("Dispute Notice & Grounds", "Client or Consultant"),
            ("Supporting Evidence & SOW References", "Disputing Party"),
            ("Rebuttal Dossier", "Responding Party"),
            ("Mediator Binding Apportionment Ruling & Rationale", "Escrow Mediator")
        ],
        "outputs": [
            ("Escrow Freeze Directive", "D9: Escrow Ledger"),
            ("Compiled Dispute Dossier", "Escrow Mediator"),
            ("Binding Fund Disbursement Execution", "M-Pesa / Bank Rails"),
            ("Adjudication Certificate PDF", "Client & Consultant"),
            ("Dispute Closure Audit Record", "D2: Audit Vault")
        ],
        "subprocesses": [
            ("7.1", "Initiate Dispute & Freeze Milestone Escrow", "Halts auto-approval timer and locks funds in dispute status."),
            ("7.2", "Assemble Dispute Dossier & Collect Rebuttals", "Enforces 48-hour evidence submission window for counter-party."),
            ("7.3", "Perform Independent Technical/Domain Audit", "Inspects code quality, legal deliverables, or tax filings."),
            ("7.4", "Issue Binding Apportionment Ruling", "Determines full release, full refund, or prorated distribution."),
            ("7.5", "Execute Adjudicated Settlement & Generate Legal Certificate", "Disburses funds and seals case in legal archive.")
        ]
    },
    {
        "id": "PROC-8.0",
        "name": "Calculate Creator Authority & Execute Platform Governance",
        "owner": "Automated Daemon / Platform Admin / Financial Auditor",
        "description": "Calculates multi-factor Creator Authority Scores (CAS), enforces anti-gaming rules, updates Redis ranking caches, executes three-way financial reconciliation, and archives statutory audits.",
        "external_entities": ["Platform Administrator", "Financial Auditor", "Kenya Revenue Authority"],
        "data_stores": [
            "D1: User & Credential Registry",
            "D2: Compliance & Audit Vault",
            "D5: Creator Authority & Telemetry Cache",
            "D9: Immutable Escrow & Financial Ledger"
        ],
        "inputs": [
            ("Hourly Cron Trigger / Major System Events", "System Clock"),
            ("Creator verification levels, escrow records, dwell logs", "D1, D2, D9"),
            ("Monthly Accounting Period Closing Trigger", "System Clock"),
            ("Bank Statements & eTIMS Registry Filings", "Bank & KRA"),
            ("Rollout Policy Directives & Take Rate Adjustments", "Platform Administrator")
        ],
        "outputs": [
            ("Normalized 0-1,000 CAS Scores & Authority Tiers", "D5 / Consultant Profile"),
            ("Redis Feed Ranking Multipliers", "D5: Telemetry Cache"),
            ("Three-Way Reconciliation Balance Sheet", "Financial Auditor"),
            ("Statutory Tax Compliance Audit Package", "KRA & Regulatory Archive"),
            ("Updated Rollout & Fee Configurations", "D8: Policy Datastore")
        ],
        "subprocesses": [
            ("8.1", "Compute Multi-Factor CAS Vectors", "Weights registry status (40%), escrow history (30%), dwell (20%), attestations (10%)."),
            ("8.2", "Apply Sybil & Anti-Gaming Dampening", "Detects circular payments and bot impressions to neutralize manipulation."),
            ("8.3", "Update High-Speed Redis Ranking Weights", "Publishes real-time ranking matrices for two-pass feed personalization."),
            ("8.4", "Perform Three-Way Ledger Reconciliation", "Matches bank statements, M-Pesa statements, and internal ledger entries."),
            ("8.5", "Seal Monthly Financial Tax Compliance Archive", "Generates immutable cryptographic audit package for KRA.")
        ]
    }
]

# Write individual process files
for proc in processes_list:
    fname = f"{proc['id'].replace('PROC-', 'PROCESS_')}_{proc['name'].replace(' ', '_').replace(',', '').replace('&', 'And').replace('/', '_')}.md"
    fpath = os.path.join(processes_dir, fname)
    
    lines = []
    lines.append(f"# Business Process Specification: {proc['name']}")
    lines.append(f"**Process ID:** `{proc['id']}` | **Owner:** {proc['owner']}\n")
    lines.append(f"### Description\n{proc['description']}\n")
    
    lines.append("### Associated External Entities")
    for ee in proc['external_entities']:
        lines.append(f"- **{ee}**")
    lines.append("")
    
    lines.append("### Associated Data Stores")
    for ds in proc['data_stores']:
        lines.append(f"- **{ds}**")
    lines.append("")
    
    lines.append("### Data Flow Analysis (Inputs & Outputs)")
    lines.append("| Flow Direction | Data Flow Name / Payload | Source / Origin | Destination |")
    lines.append("| :---: | :--- | :--- | :--- |")
    for inp in proc['inputs']:
        lines.append(f"| $\longleftarrow$ (Inflow) | {inp[0]} | {inp[1]} | `{proc['id']}` |")
    for out in proc['outputs']:
        lines.append(f"| $\longrightarrow$ (Outflow) | {out[0]} | `{proc['id']}` | {out[1]} |")
    lines.append("")
    
    lines.append("### Decomposed Sub-Processes (Level 1 DFD Scope)")
    lines.append("| Sub-Process ID | Sub-Process Name | Operational Description |")
    lines.append("| :---: | :--- | :--- |")
    for sp in proc['subprocesses']:
        lines.append(f"| **{sp[0]}** | {sp[1]} | {sp[2]} |")
    lines.append("")
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

print(f"Generated {len(processes_list)} business process specification files in {processes_dir}")
