import os

entities_dir = r"c:\Users\user\Documents\KenyaConsult\entities"
os.makedirs(entities_dir, exist_ok=True)

# 12 Core Entities categorized across Independent, Dependent, and Intersection
entities_data = [
    {
        "id": "ENT-01",
        "name": "UserAccount",
        "category": "Independent Entity (Kernel Entity)",
        "description": "Represents an authenticated human user (Client, Consultant, Admin, Mediator) in the KenyaConsult platform. Exists independently without mandatory foreign key parents.",
        "attributes": [
            ("user_id", "UUID", "PK", "Primary unique surrogate key identifier for the user."),
            ("full_name", "VARCHAR(150)", "Mandatory", "Legal name of the user."),
            ("primary_email", "VARCHAR(255)", "Mandatory, Unique", "Canonical email address used for identity and notifications."),
            ("phone_number", "VARCHAR(20)", "Mandatory, Unique", "E.164 formatted telephone number (e.g., +2547XXXXXXXX) for SMS/M-Pesa."),
            ("user_role", "ENUM('CLIENT', 'CONSULTANT', 'ADMIN', 'MEDIATOR')", "Mandatory", "Primary role controlling platform privileges."),
            ("password_hash", "VARCHAR(255)", "Mandatory", "Argon2id cryptographic hash of the account password."),
            ("mfa_secret", "VARCHAR(64)", "Optional", "TOTP multi-factor authentication seed key."),
            ("account_status", "ENUM('ACTIVE', 'SUSPENDED', 'PENDING_VERIFICATION')", "Mandatory", "Current lifecycle state of the account."),
            ("created_at", "TIMESTAMPTZ", "Mandatory", "Immutable timestamp when user registered.")
        ],
        "relationships": [
            {"target": "ConsultantProfile", "type": "Parent", "cardinality": "1 : (0,1)", "modality": "Optional", "desc": "A User may optionally have one ConsultantProfile (if role is CONSULTANT)."},
            {"target": "CaseStudyDeck", "type": "Parent", "cardinality": "1 : (0,N)", "modality": "Optional", "desc": "A User (Consultant) may author zero or many CaseStudyDecks."},
            {"target": "ConsultationBooking", "type": "Parent", "cardinality": "1 : (0,N)", "modality": "Optional", "desc": "A User (Client) may place zero or many ConsultationBookings."},
            {"target": "EscrowContract", "type": "Parent", "cardinality": "1 : (0,N)", "modality": "Optional", "desc": "A User (Client or Consultant) participates in zero or many EscrowContracts."}
        ]
    },
    {
        "id": "ENT-02",
        "name": "ConsultantProfile",
        "category": "Dependent Entity (Subtype / Characteristic Entity)",
        "description": "Maintains professional creator profile attributes, authority metrics, and Bento grid modular settings for a consultant. Dependent on UserAccount.",
        "attributes": [
            ("consultant_id", "UUID", "PK, FK (UserAccount.user_id)", "Foreign key referencing parent user and primary key."),
            ("public_handle", "VARCHAR(50)", "Mandatory, Unique", "URL slug handle (e.g., @kamau_tech) for public routing."),
            ("professional_headline", "VARCHAR(200)", "Mandatory", "Primary domain expertise tagline (e.g. 'Fintech & eTIMS Architect')."),
            ("cas_score", "DECIMAL(6,2)", "Mandatory, Default: 100.00", "Computed Creator Authority Score (0.00 to 1,000.00)."),
            ("authority_tier", "ENUM('TIER_1_EMERGING', 'TIER_2_ESTABLISHED', 'TIER_3_AUTHORITY')", "Mandatory", "Current platform authority classification."),
            ("hourly_rate_kes", "DECIMAL(10,2)", "Mandatory", "Standard advisory hourly booking rate in Kenyan Shillings."),
            ("bento_grid_layout", "JSONB", "Mandatory", "Modular widget configuration for public Bento portfolio."),
            ("total_escrow_completed", "INTEGER", "Mandatory, Default: 0", "Counter of successfully delivered escrow milestones.")
        ],
        "relationships": [
            {"target": "UserAccount", "type": "Child", "cardinality": "(1,1) : 1", "modality": "Mandatory", "desc": "Each ConsultantProfile must belong to exactly one UserAccount."},
            {"target": "ProfessionalCredential", "type": "Parent", "cardinality": "1 : (0,N)", "modality": "Optional", "desc": "A ConsultantProfile may hold zero or many ProfessionalCredentials."},
            {"target": "CaseStudyDeck", "type": "Parent", "cardinality": "1 : (0,N)", "modality": "Optional", "desc": "A ConsultantProfile owns zero or many CaseStudyDecks."}
        ]
    },
    {
        "id": "ENT-03",
        "name": "ProfessionalCredential",
        "category": "Dependent Entity (Weak Entity)",
        "description": "Represents statutory professional certifications (LSK, ICPAK, EBK) and national identity documents submitted for regulatory validation. Dependent on ConsultantProfile.",
        "attributes": [
            ("credential_id", "UUID", "PK", "Primary surrogate key identifier for the credential entry."),
            ("consultant_id", "UUID", "FK (ConsultantProfile.consultant_id)", "Mandatory reference to owning consultant."),
            ("credential_type", "ENUM('NATIONAL_ID', 'KRA_PIN', 'LSK_ADVOCATE', 'ICPAK_CPA', 'EBK_ENGINEER')", "Mandatory", "Type of professional board or national credential."),
            ("license_number", "VARCHAR(100)", "Mandatory", "Official practicing certificate or registration number."),
            ("verification_status", "ENUM('PENDING', 'VERIFIED_ACTIVE', 'REJECTED', 'EXPIRED')", "Mandatory", "Current verification status from statutory registry."),
            ("registry_response_hash", "VARCHAR(64)", "Optional", "SHA-256 hash of official API response for immutable audit trail."),
            ("verified_at", "TIMESTAMPTZ", "Optional", "Timestamp when automated check or compliance officer confirmed validity."),
            ("expiry_date", "DATE", "Optional", "Statutory expiration date of practicing license.")
        ],
        "relationships": [
            {"target": "ConsultantProfile", "type": "Child", "cardinality": "(1,1) : 1", "modality": "Mandatory", "desc": "Each credential strictly belongs to exactly one ConsultantProfile."}
        ]
    },
    {
        "id": "ENT-04",
        "name": "CaseStudyDeck",
        "category": "Independent Entity (Core Content Kernel)",
        "description": "A modular, visual-first technical or advisory case study created in Creation Studio. Can exist and be viewed independently within the content catalog.",
        "attributes": [
            ("case_study_id", "UUID", "PK", "Primary surrogate key identifier for the case study."),
            ("author_id", "UUID", "FK (ConsultantProfile.consultant_id)", "Mandatory author reference."),
            ("case_title", "VARCHAR(255)", "Mandatory", "Display title of the case study."),
            ("slug", "VARCHAR(255)", "Mandatory, Unique", "SEO-optimized URI slug."),
            ("executive_summary", "TEXT", "Mandatory", "Concise problem-solution-impact narrative."),
            ("content_blueprint_json", "JSONB", "Mandatory", "Structured sections containing markdown, metrics, and Mermaid definitions."),
            ("conversion_anchor_json", "JSONB", "Mandatory", "Configuration for embedded booking drawer and call-to-action."),
            ("publication_status", "ENUM('DRAFT', 'PUBLISHED', 'UNDER_MODERATION', 'REDACTED')", "Mandatory", "Lifecycle state."),
            ("view_count", "INTEGER", "Mandatory, Default: 0", "Cumulative client view impressions."),
            ("bookmark_count", "INTEGER", "Mandatory, Default: 0", "Total times saved to client collections."),
            ("published_at", "TIMESTAMPTZ", "Optional", "Timestamp when case study was made publicly visible.")
        ],
        "relationships": [
            {"target": "ConsultantProfile", "type": "Child", "cardinality": "(1,1) : 1", "modality": "Mandatory", "desc": "Authored by exactly one ConsultantProfile."},
            {"target": "ExecutionProof", "type": "Parent", "cardinality": "1 : (0,N)", "modality": "Optional", "desc": "May attach zero or many verifiable ExecutionProofs."},
            {"target": "CaseStudyTagIntersection", "type": "Parent", "cardinality": "1 : (0,N)", "modality": "Optional", "desc": "Categorized into zero or many TopicTags."},
            {"target": "UserBookmarkIntersection", "type": "Parent", "cardinality": "1 : (0,N)", "modality": "Optional", "desc": "Bookmarked by zero or many Users."}
        ]
    },
    {
        "id": "ENT-05",
        "name": "ExecutionProof",
        "category": "Dependent Entity (Characteristic Entity)",
        "description": "Verifiable evidence item linked to claims in a case study (GitHub commit, live URL, client co-sign, PDF audit memo). Dependent on CaseStudyDeck.",
        "attributes": [
            ("proof_id", "UUID", "PK", "Primary surrogate key identifier for the proof asset."),
            ("case_study_id", "UUID", "FK (CaseStudyDeck.case_study_id)", "Mandatory reference to parent case study."),
            ("proof_type", "ENUM('GITHUB_COMMIT', 'LIVE_URL', 'CLIENT_COSIGN', 'AUDIT_MEMO_PDF')", "Mandatory", "Classification of proof."),
            ("external_uri", "VARCHAR(500)", "Optional", "Direct link to external repository commit or production system."),
            ("sha256_fingerprint", "CHAR(64)", "Mandatory", "Cryptographic SHA-256 hash verifying asset integrity."),
            ("is_externally_verified", "BOOLEAN", "Mandatory, Default: FALSE", "Flag set to TRUE upon successful GitHub API or signature validation."),
            ("created_at", "TIMESTAMPTZ", "Mandatory", "Timestamp of proof registration.")
        ],
        "relationships": [
            {"target": "CaseStudyDeck", "type": "Child", "cardinality": "(1,1) : 1", "modality": "Mandatory", "desc": "Must be attached to exactly one parent CaseStudyDeck."}
        ]
    },
    {
        "id": "ENT-06",
        "name": "TopicTag",
        "category": "Independent Entity (Lookup / Taxonomy Entity)",
        "description": "Standardized taxonomy keywords and industry classifications (e.g., #FintechCompliance, #KRAeTIMS, #SoftwareArchitecture) used for two-pass discovery indexing.",
        "attributes": [
            ("tag_id", "UUID", "PK", "Primary surrogate key identifier for the topic tag."),
            ("tag_name", "VARCHAR(60)", "Mandatory, Unique", "Display keyword hashtag without spaces."),
            ("category_domain", "VARCHAR(60)", "Mandatory", "Broader professional domain (e.g., Legal, Tax, Engineering)."),
            ("is_featured", "BOOLEAN", "Mandatory, Default: FALSE", "Flag indicating prominent home feed placement.")
        ],
        "relationships": [
            {"target": "CaseStudyTagIntersection", "type": "Parent", "cardinality": "1 : (0,N)", "modality": "Optional", "desc": "Applied to zero or many CaseStudyDecks."}
        ]
    },
    {
        "id": "ENT-07",
        "name": "CaseStudyTagIntersection",
        "category": "Intersection Entity (Associative Entity: M:N Resolver)",
        "description": "Resolves the Many-to-Many (M:N) relationship between CaseStudyDeck and TopicTag. Contains composite foreign keys and ranking relevance weight.",
        "attributes": [
            ("case_study_id", "UUID", "PK, FK (CaseStudyDeck.case_study_id)", "Foreign key referencing case study."),
            ("tag_id", "UUID", "PK, FK (TopicTag.tag_id)", "Foreign key referencing topic tag."),
            ("relevance_score", "DECIMAL(4,3)", "Mandatory, Default: 1.000", "Semantic affinity weight between tag and deck."),
            ("assigned_at", "TIMESTAMPTZ", "Mandatory", "Timestamp when tag association was created.")
        ],
        "relationships": [
            {"target": "CaseStudyDeck", "type": "Child", "cardinality": "(1,1) : 1", "modality": "Mandatory", "desc": "Connects to one CaseStudyDeck."},
            {"target": "TopicTag", "type": "Child", "cardinality": "(1,1) : 1", "modality": "Mandatory", "desc": "Connects to one TopicTag."}
        ]
    },
    {
        "id": "ENT-08",
        "name": "UserBookmarkIntersection",
        "category": "Intersection Entity (Associative Entity: M:N Resolver)",
        "description": "Resolves the Many-to-Many (M:N) relationship between UserAccount and CaseStudyDeck for saved collections. Emits high-value 5x algorithmic signals.",
        "attributes": [
            ("user_id", "UUID", "PK, FK (UserAccount.user_id)", "Foreign key referencing saving user."),
            ("case_study_id", "UUID", "PK, FK (CaseStudyDeck.case_study_id)", "Foreign key referencing saved case study."),
            ("collection_name", "VARCHAR(100)", "Mandatory, Default: 'Default'", "User-defined named collection folder."),
            ("saved_at", "TIMESTAMPTZ", "Mandatory", "Timestamp when bookmark was saved.")
        ],
        "relationships": [
            {"target": "UserAccount", "type": "Child", "cardinality": "(1,1) : 1", "modality": "Mandatory", "desc": "Saved by exactly one UserAccount."},
            {"target": "CaseStudyDeck", "type": "Child", "cardinality": "(1,1) : 1", "modality": "Mandatory", "desc": "Points to exactly one CaseStudyDeck."}
        ]
    },
    {
        "id": "ENT-09",
        "name": "ConsultationBooking",
        "category": "Independent / Operational Transaction Entity",
        "description": "Represents a scheduled 1-on-1 advisory session between a Client and a Consultant. Manages calendar slots, WebRTC room credentials, and session state.",
        "attributes": [
            ("booking_id", "UUID", "PK", "Primary surrogate key identifier for the booking."),
            ("client_id", "UUID", "FK (UserAccount.user_id)", "Mandatory client reference."),
            ("consultant_id", "UUID", "FK (ConsultantProfile.consultant_id)", "Mandatory consultant reference."),
            ("case_study_anchor_id", "UUID", "Optional, FK (CaseStudyDeck.case_study_id)", "Optional originating case study CTA."),
            ("scheduled_start_time", "TIMESTAMPTZ", "Mandatory", "Agreed consultation starting timestamp (EAT)."),
            ("duration_minutes", "INTEGER", "Mandatory, Default: 45", "Length of consultation in minutes."),
            ("session_status", "ENUM('PENDING_PAYMENT', 'CONFIRMED', 'IN_SESSION', 'COMPLETED', 'CANCELLED', 'NO_SHOW')", "Mandatory", "Lifecycle state."),
            ("webrtc_room_token", "VARCHAR(255)", "Optional", "Encrypted media room access token."),
            ("total_fee_kes", "DECIMAL(10,2)", "Mandatory", "Total session fee charged in Kenyan Shillings."),
            ("created_at", "TIMESTAMPTZ", "Mandatory", "Timestamp when slot reservation was initiated.")
        ],
        "relationships": [
            {"target": "UserAccount", "type": "Child", "cardinality": "(1,1) : 1", "modality": "Mandatory", "desc": "Booked by exactly one Client."},
            {"target": "ConsultantProfile", "type": "Child", "cardinality": "(1,1) : 1", "modality": "Mandatory", "desc": "Delivered by exactly one Consultant."},
            {"target": "EscrowContract", "type": "Parent", "cardinality": "1 : (0,1)", "modality": "Optional", "desc": "Tied to zero or one parent EscrowContract."},
            {"target": "LedgerTransaction", "type": "Parent", "cardinality": "1 : (1,N)", "modality": "Mandatory", "desc": "Has one or many LedgerTransactions."}
        ]
    },
    {
        "id": "ENT-10",
        "name": "EscrowContract",
        "category": "Independent / Operational Contract Entity",
        "description": "Represents a formal Statement of Work (SOW) consulting agreement or high-value advisory engagement with funds held in trust across defined milestones.",
        "attributes": [
            ("contract_id", "UUID", "PK", "Primary surrogate key identifier for the escrow contract."),
            ("client_id", "UUID", "FK (UserAccount.user_id)", "Mandatory hiring client reference."),
            ("consultant_id", "UUID", "FK (ConsultantProfile.consultant_id)", "Mandatory delivering consultant reference."),
            ("contract_title", "VARCHAR(200)", "Mandatory", "Formal title of Statement of Work."),
            ("contract_status", "ENUM('DRAFT', 'FUNDED_ACTIVE', 'IN_DISPUTE', 'COMPLETED_RELEASED', 'REFUNDED')", "Mandatory", "Lifecycle state."),
            ("total_contract_value_kes", "DECIMAL(12,2)", "Mandatory", "Aggregated value of all milestone tranches in KES."),
            ("platform_commission_rate", "DECIMAL(4,4)", "Mandatory, Default: 0.0700", "Platform take rate (e.g. 7.00%)."),
            ("created_at", "TIMESTAMPTZ", "Mandatory", "Timestamp when contract was drafted.")
        ],
        "relationships": [
            {"target": "UserAccount", "type": "Child", "cardinality": "(1,1) : 1", "modality": "Mandatory", "desc": "Contracted by exactly one Client."},
            {"target": "ConsultantProfile", "type": "Child", "cardinality": "(1,1) : 1", "modality": "Mandatory", "desc": "Delivered by exactly one Consultant."},
            {"target": "EscrowMilestone", "type": "Parent", "cardinality": "1 : (1,N)", "modality": "Mandatory", "desc": "Composed of one or many EscrowMilestones."},
            {"target": "DisputeCase", "type": "Parent", "cardinality": "1 : (0,N)", "modality": "Optional", "desc": "May have zero or many DisputeCases."}
        ]
    },
    {
        "id": "ENT-11",
        "name": "EscrowMilestone",
        "category": "Dependent Entity (Sub-Contract Tranche Entity)",
        "description": "An atomic phase within an EscrowContract with specific deliverables, due date, inspection timer, and escrow release sum. Dependent on EscrowContract.",
        "attributes": [
            ("milestone_id", "UUID", "PK", "Primary surrogate key identifier for the milestone."),
            ("contract_id", "UUID", "FK (EscrowContract.contract_id)", "Mandatory reference to parent contract."),
            ("sequence_number", "SMALLINT", "Mandatory", "Sequential order (e.g. 1, 2, 3) of milestone."),
            ("milestone_title", "VARCHAR(150)", "Mandatory", "Descriptive phase name (e.g. 'Architecture Blueprint')."),
            ("milestone_amount_kes", "DECIMAL(12,2)", "Mandatory", "Principal amount locked in escrow for this tranche."),
            ("milestone_status", "ENUM('PENDING_FUNDING', 'FUNDED_LOCKED', 'SUBMITTED', 'REVISIONS_REQUESTED', 'APPROVED_RELEASED', 'FROZEN_DISPUTE')", "Mandatory", "State of the milestone."),
            ("deliverable_sha256", "CHAR(64)", "Optional", "Cryptographic fingerprint of submitted artifacts."),
            ("inspection_deadline", "TIMESTAMPTZ", "Optional", "72-hour auto-approval deadline timestamp."),
            ("approved_at", "TIMESTAMPTZ", "Optional", "Timestamp when funds were authorized for release.")
        ],
        "relationships": [
            {"target": "EscrowContract", "type": "Child", "cardinality": "(1,1) : 1", "modality": "Mandatory", "desc": "Belongs strictly to exactly one EscrowContract."},
            {"target": "DisputeCase", "type": "Parent", "cardinality": "1 : (0,1)", "modality": "Optional", "desc": "May be subject to zero or one DisputeCase."},
            {"target": "LedgerTransaction", "type": "Parent", "cardinality": "1 : (1,N)", "modality": "Mandatory", "desc": "Produces one or many LedgerTransactions."}
        ]
    },
    {
        "id": "ENT-12",
        "name": "LedgerTransaction",
        "category": "Dependent Entity (Immutable Financial Double-Entry Record)",
        "description": "An immutable double-entry journal entry tracking money movement across payment rails, platform commission, trust escrow, and B2C payouts. Dependent on Booking or Milestone.",
        "attributes": [
            ("transaction_id", "UUID", "PK", "Primary surrogate key identifier for the ledger row."),
            ("booking_id", "UUID", "Optional, FK (ConsultationBooking.booking_id)", "Optional reference to consultation booking."),
            ("milestone_id", "UUID", "Optional, FK (EscrowMilestone.milestone_id)", "Optional reference to escrow milestone."),
            ("debit_account", "VARCHAR(50)", "Mandatory", "Double-entry debit account (e.g., 'ESCROW_TRUST_CASH', 'CLIENT_FUNDS')."),
            ("credit_account", "VARCHAR(50)", "Mandatory", "Double-entry credit account (e.g., 'CONSULTANT_PAYABLE', 'PLATFORM_REVENUE')."),
            ("amount_kes", "DECIMAL(12,2)", "Mandatory", "Exact monetary amount in Kenyan Shillings."),
            ("payment_rail", "ENUM('MPESA_DARAYA', 'CARD_PAYSTACK', 'RTGS_WIRE', 'MPESA_B2C')", "Mandatory", "Fintech rail utilized."),
            ("external_reference", "VARCHAR(100)", "Mandatory, Unique", "Safaricom M-Pesa receipt code or bank transaction reference."),
            ("etims_invoice_number", "VARCHAR(100)", "Optional", "KRA eTIMS statutory tax invoice code."),
            ("created_at", "TIMESTAMPTZ", "Mandatory", "Immutable timestamp when entry was recorded.")
        ],
        "relationships": [
            {"target": "ConsultationBooking", "type": "Child", "cardinality": "(0,1) : 1", "modality": "Optional", "desc": "Linked to at most one ConsultationBooking."},
            {"target": "EscrowMilestone", "type": "Child", "cardinality": "(0,1) : 1", "modality": "Optional", "desc": "Linked to at most one EscrowMilestone."}
        ]
    }
]

# Write individual entity files
for ent in entities_data:
    fname = f"{ent['id']}_{ent['name']}.md"
    fpath = os.path.join(entities_dir, fname)
    
    lines = []
    lines.append(f"# Entity Specification: {ent['name']}")
    lines.append(f"**Entity ID:** `{ent['id']}` | **Category:** {ent['category']}\n")
    lines.append(f"### Description\n{ent['description']}\n")
    
    lines.append("### Attribute Data Dictionary")
    lines.append("| Attribute Name | Data Type | Key / Constraint | Functional Description |")
    lines.append("| :--- | :--- | :--- | :--- |")
    for attr in ent['attributes']:
        lines.append(f"| **`{attr[0]}`** | `{attr[1]}` | {attr[2]} | {attr[3]} |")
    lines.append("")
    
    lines.append("### Relationships & Structural Constraints")
    lines.append("| Target Entity | Direction | Cardinality | Modality | Semantic Business Rule |")
    lines.append("| :--- | :---: | :---: | :---: | :--- |")
    for rel in ent['relationships']:
        lines.append(f"| **`{rel['target']}`** | {rel['type']} | `{rel['cardinality']}` | {rel['modality']} | {rel['desc']} |")
    lines.append("")
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

print(f"Generated {len(entities_data)} entity specifications in {entities_dir}")
