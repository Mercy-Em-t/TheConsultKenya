import os

output_dir = r"c:\Users\user\Documents\KenyaConsult\use_cases"
os.makedirs(output_dir, exist_ok=True)

# 22 Core Use Cases with deep Dennis-Wixom / Tegarden structure matching the user's reference diagram
use_cases_data = [
    {
        "id": "UC-01",
        "name": "Discover Content via Dual-Mode Feeds",
        "priority": "High",
        "actor": "Client / Enterprise Buyer (also Guest Visitor)",
        "description": "The Client accesses the Consult Kenya discovery feed to explore authoritative business and technical case studies through either a vertical TikTok-style micro-feed or a curated horizontal topic carousel. The system tailors the feed using Creator Authority Scores (CAS) and engagement telemetry.",
        "trigger": "Client launches mobile/web app or navigates to the home feed to discover domain insights.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Client device has network connectivity or cached local feed state.",
            "2. Recommendation engine and vector database are operational.",
            "3. Case study repository contains verified published decks."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Browse dual-mode discovery feed", "flow": "", "info": "Feed Initialization"},
            {"step": "1", "action": "Client opens home feed and selects preferred viewing mode (Vertical Feed vs. Horizontal Carousels)", "flow": "<-", "info": "Feed mode preference (swipe / grid)"},
            {"step": "2", "action": "System queries recommendation engine with client persona, topic history, and geo-filter (East Africa / Kenya)", "flow": "<-", "info": "Client session profile & geo-tag"},
            {"step": "3", "action": "System ranks published case studies using CAS weight and engagement decay", "flow": "<-", "info": "Scored case study candidate list"},
            {"step": "4", "action": "System streams first page of case study previews (video snippet, title, author Bento card, metrics)", "flow": "->", "info": "Ranked feed card array"},
            {"step": "5", "action": "Client scrolls or swipes through cards, dwelling on specific case study", "flow": "<-", "info": "Dwell time telemetry & interaction event"},
            {"step": "6", "action": "System records dwell telemetry and dynamically pre-buffers full case study assets (Mermaid charts, proofs)", "flow": "->", "info": "Pre-buffered case study deck"},
            {"step": "7", "action": "Client taps card to expand full case study presentation", "flow": "<-", "info": "Card expansion selection"},
            {"step": "8", "action": "System renders interactive case study with author conversion CTA anchor", "flow": "->", "info": "Full interactive case study view"}
        ],
        "alternatives": [
            {
                "id": "1.1",
                "title": "Client filters by specific industry topic or hashtag (branch at step 1)",
                "steps": [
                    {"step": "1", "action": "Client selects topic filter badge (e.g. #FintechCompliance, #KRAeTIMS, #AgriTech)", "flow": "<-", "info": "Selected topic tag"},
                    {"step": "2a", "action": "System queries vector engine filtered strictly by requested taxonomy", "flow": "<-", "info": "Taxonomy query filter"},
                    {"step": "3a", "action": "System renders topic-focused sub-feed sorted by CAS rating", "flow": "->", "info": "Topic-filtered case study array"},
                    {"step": "4a", "action": "System resumes Normal Course at step 5", "flow": "", "info": "Resume workflow"}
                ]
            },
            {
                "id": "1.2",
                "title": "Offline / low-bandwidth fallback (branch at step 2)",
                "steps": [
                    {"step": "1", "action": "System detects network degradation (<50 kbps or offline)", "flow": "<-", "info": "Network latency status"},
                    {"step": "2a", "action": "System serves locally cached lightweight SQLite summary cards without rich video", "flow": "->", "info": "Cached summary cards"},
                    {"step": "3a", "action": "System queues user interaction events into local IndexedDB for delayed sync", "flow": "->", "info": "Queued telemetry log"}
                ]
            }
        ],
        "postconditions": [
            "1. Client view history is updated in the telemetry database.",
            "2. Creator of the viewed case study receives dwell-time impression signal.",
            "3. Client session state preserves feed scroll position."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Feed generation timeout or service unavailability (occurs at step 3)",
                "steps": [
                    "1. System displays graceful fallback message: 'Live recommendation unavailable. Loading trending case studies.'",
                    "2. System serves static cached trending leaderboard.",
                    "3. System logs warning to platform telemetry aggregator."
                ]
            }
        ],
        "inputs": [
            ("Client session profile & mode toggle", "Client Browser / Mobile App"),
            ("Case study index & CAS weights", "Recommendation Database / Redis Cache"),
            ("Dwell time telemetry", "Client Telemetry Tracker")
        ],
        "outputs": [
            ("Ranked Feed Card Stream", "Client Display UI"),
            ("Pre-buffered Case Study Deck", "Client Memory Store"),
            ("Impression & Dwell Telemetry", "Analytics Logging Engine")
        ],
        "fr_correlation": ["FR-001 (Content Ingestion & Delivery)", "FR-018 (Algorithmic Feed Personalization)", "FR-022 (Offline Caching)"],
        "testing_mapping": {
            "positive_tests": ["TC-01-01: Verify default personalized dual-mode feed renders within 800ms.", "TC-01-02: Verify switching to horizontal carousel preserves current focus."],
            "boundary_tests": ["TC-01-03: Verify feed performance with 10,000+ cached items under slow 3G network."],
            "exception_tests": ["TC-01-04: Verify recommendation engine outage triggers cached trending fallback."]
        }
    },
    {
        "id": "UC-02",
        "name": "Inspect Consultant Portfolio (Bento Grid)",
        "priority": "High",
        "actor": "Client / Enterprise Buyer",
        "description": "The Client views a consultant's public authority profile presented as a high-density, modular Bento grid. The profile displays verified professional credentials, live booking rates, featured visual case studies, execution proofs, and client reviews.",
        "trigger": "Client clicks on a consultant's avatar, handle, or author badge from a case study or search result.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Consultant profile exists and has completed minimum profile onboarding.",
            "2. Consultant public visibility is set to active."
        ],
        "normal_course": [
            {"step": "1.0", "action": "View consultant authority Bento portfolio", "flow": "", "info": "Profile Request"},
            {"step": "1", "action": "Client requests consultant profile by handle or ID", "flow": "<-", "info": "Consultant Handle / ID"},
            {"step": "2", "action": "System retrieves verified credentials, CAS score, bio, and Bento grid modules", "flow": "<-", "info": "Consultant Profile Datastore"},
            {"step": "3", "action": "System retrieves active booking packages, availability calendar, and escrow history", "flow": "<-", "info": "Booking & Escrow DB"},
            {"step": "4", "action": "System renders Bento Grid: [Bio & Tier Badge | Featured Case Studies | Booking Widget | Verification Seals | Client Proofs]", "flow": "->", "info": "Modular Bento Grid UI"},
            {"step": "5", "action": "Client inspects verified credential seals (e.g. LSK, ICPAK, EBK, GitHub)", "flow": "<-", "info": "Badge inspection tap"},
            {"step": "6", "action": "System presents cryptographic validation modal verifying external registry confirmation", "flow": "->", "info": "Registry verification modal"},
            {"step": "7", "action": "Client reviews consultant past project ratings and escrow completion rate", "flow": "->", "info": "Escrow completion statistics"}
        ],
        "alternatives": [
            {
                "id": "2.1",
                "title": "Consultant has zero published case studies (brand new onboarded creator)",
                "steps": [
                    {"step": "1", "action": "System detects empty case study portfolio", "flow": "<-", "info": "Empty deck flag"},
                    {"step": "2a", "action": "System renders Bento layout highlighting verified identity, academic qualifications, and intro advisory call offer", "flow": "->", "info": "Starter Bento template"}
                ]
            }
        ],
        "postconditions": [
            "1. Profile view counter incremented for consultant analytics.",
            "2. Client recently-viewed consultant stack updated."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Consultant profile is suspended or under moderation review",
                "steps": [
                    "1. System displays notice: 'This consultant profile is currently under review.'",
                    "2. System restricts booking button and redirects user to topic search."
                ]
            }
        ],
        "inputs": [
            ("Consultant Handle / ID", "Client Navigation"),
            ("Credential & Verification records", "Identity Verification Datastore"),
            ("Consultant engagement metrics", "CAS Telemetry Database")
        ],
        "outputs": [
            ("Bento Grid Profile Layout", "Client UI"),
            ("Cryptographic Registry Proof", "Verification Modal UI")
        ],
        "fr_correlation": ["FR-002 (Bento Profile Architecture)", "FR-008 (Credential Verification Display)", "FR-009 (Booking Anchor Integration)"],
        "testing_mapping": {
            "positive_tests": ["TC-02-01: Verify Bento grid renders all 6 modules within 500ms.", "TC-02-02: Verify verification seals open valid modal with registry timestamp."],
            "boundary_tests": ["TC-02-03: Verify layout responsiveness on both 360px mobile screen and 4K ultra-wide monitor."],
            "exception_tests": ["TC-02-04: Verify suspended profile hides booking triggers and displays compliant notice."]
        }
    },
    {
        "id": "UC-03",
        "name": "Search & Filter Topic Hubs",
        "priority": "High",
        "actor": "Client / Enterprise Buyer",
        "description": "The Client searches for specialized advisors, legal/financial expertise, or technical case studies using natural language queries, keyword tags, or structured filters (e.g., industry, pricing tier, verified board membership).",
        "trigger": "Client enters a search query in the search bar or selects a topic category hub.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Search index and vector embeddings are up to date.",
            "2. Minimum query length is 2 characters or valid tag filter selected."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Perform semantic and structured topic search", "flow": "", "info": "Search Execution"},
            {"step": "1", "action": "Client types search query (e.g. 'eTIMS system integration Kenya') or selects topic badge", "flow": "<-", "info": "Raw query string / Tag ID"},
            {"step": "2", "action": "System executes Pass-1 candidate retrieval across full-text index and vector embedding store", "flow": "<-", "info": "Vector Cosine Search"},
            {"step": "3", "action": "System retrieves matching case studies, verified consultants, and discussion threads", "flow": "<-", "info": "Candidate hit set"},
            {"step": "4", "action": "System ranks results applying Creator Authority Scores and relevance thresholds", "flow": "<-", "info": "CAS Scored Ranking"},
            {"step": "5", "action": "System presents segmented search result view: [Top Consultants | Relevant Case Studies | Topic Tags]", "flow": "->", "info": "Segmented Search Results View"},
            {"step": "6", "action": "Client applies facet filters (Hourly Rate: KES 5,000-15,000, LSK Certified, Rating > 4.8)", "flow": "<-", "info": "Facet filter criteria"},
            {"step": "7", "action": "System re-renders filtered list instantaneously (<100ms via client-side cache)", "flow": "->", "info": "Refined result list"}
        ],
        "alternatives": [
            {
                "id": "3.1",
                "title": "No direct matches found (Zero Results Query)",
                "steps": [
                    {"step": "1", "action": "System detects zero candidate matches", "flow": "<-", "info": "Empty hit set"},
                    {"step": "2a", "action": "System provides phonetic 'Did you mean?' suggestions and related topic hubs", "flow": "->", "info": "Fuzzy suggestions & related hubs"},
                    {"step": "3a", "action": "Client selects recommended alternative hub", "flow": "<-", "info": "Alternative hub selection"},
                    {"step": "4a", "action": "System resumes Normal Course at step 5", "flow": "", "info": "Resume workflow"}
                ]
            }
        ],
        "postconditions": [
            "1. Search telemetry logged for keyword trend analysis.",
            "2. Client search history cached locally for instant revisit."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Vector search engine timeout",
                "steps": [
                    "1. System falls back automatically to PostgreSQL full-text search (tsvector).",
                    "2. Results served with non-blocking warning flag."
                ]
            }
        ],
        "inputs": [
            ("Query string and facet filters", "Client Search Input"),
            ("Vector embeddings & Full-text index", "Elasticsearch / pgvector Datastore")
        ],
        "outputs": [
            ("Segmented Search Results UI", "Client Display"),
            ("Query telemetry log", "Platform Search Analytics")
        ],
        "fr_correlation": ["FR-003 (Semantic Search & Filtering)", "FR-018 (Two-Pass Retrieval)"],
        "testing_mapping": {
            "positive_tests": ["TC-03-01: Verify natural language query 'KRA audit tax consultant' returns top-3 LSK/ICPAK certified experts."],
            "boundary_tests": ["TC-03-02: Test query with special characters, emojis, and maximum string length (256 chars)."],
            "exception_tests": ["TC-03-03: Verify graceful fallback to SQL LIKE search when vector store latency exceeds 300ms."]
        }
    },
    {
        "id": "UC-04",
        "name": "Bookmark & Organize Case Studies",
        "priority": "Medium",
        "actor": "Client / Enterprise Buyer",
        "description": "The Client bookmarks case studies, technical blueprints, or checklists into custom private or team collections. Bookmarks signal high intent to the algorithmic discovery engine.",
        "trigger": "Client clicks the bookmark/save icon on a case study card or deck.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Client is authenticated.",
            "2. Case study is active and accessible."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Save case study to organized collection", "flow": "", "info": "Bookmark Action"},
            {"step": "1", "action": "Client clicks 'Bookmark' icon on a case study card", "flow": "<-", "info": "Bookmark trigger"},
            {"step": "2", "action": "System displays modal with existing collections and '+ New Collection' option", "flow": "->", "info": "Collection list modal"},
            {"step": "3", "action": "Client chooses target collection (e.g., 'Q3 Tech Stack Architecture')", "flow": "<-", "info": "Selected Collection ID"},
            {"step": "4", "action": "System saves bookmark record into User Collections datastore", "flow": "->", "info": "Bookmark Record"},
            {"step": "5", "action": "System emits high-weight algorithmic event (5x save multiplier) to CAS engine for creator", "flow": "->", "info": "Algorithmic save signal"},
            {"step": "6", "action": "System presents confirmation toast: 'Saved to Q3 Tech Stack Architecture'", "flow": "->", "info": "Confirmation toast"}
        ],
        "alternatives": [
            {
                "id": "4.1",
                "title": "Client creates a new collection on the fly (branch at step 3)",
                "steps": [
                    {"step": "1", "action": "Client enters new collection name and privacy toggle (Private / Team Shared)", "flow": "<-", "info": "New collection metadata"},
                    {"step": "2a", "action": "System creates new collection entity and adds selected case study", "flow": "->", "info": "Created collection entity"},
                    {"step": "3a", "action": "System proceeds to step 5 of Normal Course", "flow": "", "info": "Resume workflow"}
                ]
            }
        ],
        "postconditions": [
            "1. Case study is accessible in client's Saved library.",
            "2. Creator's case study save tally incremented by 1."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Duplicate bookmark attempted",
                "steps": [
                    "1. System alerts: 'Already in collection. Would you like to move or remove?'",
                    "2. Client can un-bookmark or cancel without error."
                ]
            }
        ],
        "inputs": [
            ("Case Study ID & Collection selection", "Client Input"),
            ("Existing collections list", "User Profile Datastore")
        ],
        "outputs": [
            ("Updated Bookmark Record", "User Collections Database"),
            ("5x CAS Engagement Signal", "Recommendation Pipeline")
        ],
        "fr_correlation": ["FR-004 (Bookmark & Collection Management)", "FR-017 (CAS Telemetry Tracking)"],
        "testing_mapping": {
            "positive_tests": ["TC-04-01: Verify bookmarking persists across page reloads and mobile apps."],
            "boundary_tests": ["TC-04-02: Test maximum collection name length (100 chars) and 500+ bookmarks in a single folder."],
            "exception_tests": ["TC-04-03: Verify handling of bookmarked case studies if creator deletes or unpublishes deck."]
        }
    },
    {
        "id": "UC-05",
        "name": "Compose Case Study via Creation Studio",
        "priority": "High",
        "actor": "Consultant / Specialist Creator",
        "description": "The Consultant creates a high-impact, visual-first case study using the modular Creation Studio. The studio provides structured sections (Executive Summary, Challenge, Solution Blueprint, Technical Architecture, Measurable Impact), Markdown/Mermaid diagram rendering, syntax highlighting, and live split-screen preview.",
        "trigger": "Consultant clicks '+ Create Case Study' in Creator Dashboard.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Consultant is authenticated and has verified creator permissions.",
            "2. Creation Studio storage and asset CDN are available."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Author and publish structured visual case study", "flow": "", "info": "Studio Authoring"},
            {"step": "1", "action": "Consultant selects case study template (e.g. 'Software Architecture Audit', 'Tax Optimization', 'Legal Memo')", "flow": "<-", "info": "Selected Template ID"},
            {"step": "2", "action": "System populates modular editor canvas with structured sections (Challenge, Solution, Impact)", "flow": "->", "info": "Initialized editor canvas"},
            {"step": "3", "action": "Consultant enters case title, problem statement, and metric callouts (e.g. '99.99% Uptime', 'KES 14M Saved')", "flow": "<-", "info": "Case study content & metrics"},
            {"step": "4", "action": "Consultant embeds Mermaid architecture diagrams or code syntax blocks", "flow": "<-", "info": "Mermaid / Code text block"},
            {"step": "5", "action": "System parses Mermaid syntax and renders live visual diagram in split preview", "flow": "->", "info": "Rendered SVG architecture"},
            {"step": "6", "action": "System performs automatic auto-save every 30 seconds into draft datastore", "flow": "->", "info": "Draft save state"},
            {"step": "7", "action": "Consultant previews mobile and desktop responsiveness", "flow": "<-", "info": "Preview mode toggle"},
            {"step": "8", "action": "Consultant clicks 'Proceed to Attach Evidence & CTA' (triggers UC-06 & UC-07)", "flow": "<-", "info": "Proceed action"}
        ],
        "alternatives": [
            {
                "id": "5.1",
                "title": "Syntax error in Mermaid diagram definition (branch at step 5)",
                "steps": [
                    {"step": "1", "action": "System parser flags syntax error with line number and human-readable suggestion", "flow": "->", "info": "Mermaid parser lint error"},
                    {"step": "2a", "action": "Consultant corrects invalid token in editor", "flow": "<-", "info": "Corrected diagram text"},
                    {"step": "3a", "action": "System re-parses and displays valid SVG diagram", "flow": "->", "info": "Valid rendered diagram"}
                ]
            }
        ],
        "postconditions": [
            "1. Draft case study saved in consultant's workspace with unique version identifier.",
            "2. System confirms all assets and diagrams are pre-rendered and cached."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Session disconnect or sudden browser close during drafting",
                "steps": [
                    "1. Local storage auto-sync recovers last uncommitted keystrokes upon re-opening.",
                    "2. Consultant prompted: 'Recover unsaved draft from 2 minutes ago?'"
                ]
            }
        ],
        "inputs": [
            ("Template selection & Case study markdown text", "Consultant Authoring"),
            ("Mermaid syntax definitions & Code blocks", "Consultant Input")
        ],
        "outputs": [
            ("Live Rendered SVG / Visual Cards", "Editor Preview Canvas"),
            ("Persisted Draft Document Entity", "Creation Studio Database")
        ],
        "fr_correlation": ["FR-005 (Creation Studio Engine)", "FR-006 (Diagramming & Code Rendering)"],
        "testing_mapping": {
            "positive_tests": ["TC-05-01: Verify valid Mermaid flowchart renders cleanly within 200ms of typing."],
            "boundary_tests": ["TC-05-02: Test maximum case study word count (10,000 words) and 15 nested diagrams."],
            "exception_tests": ["TC-05-03: Verify corrupt markdown does not break client-side layout or crash editor."]
        }
    },
    {
        "id": "UC-06",
        "name": "Tag Evidence & Proof of Execution",
        "priority": "High",
        "actor": "Consultant / Specialist Creator",
        "description": "The Consultant links concrete, verifiable evidence to the case study (such as GitHub/GitLab repository commit tags, live production URLs, anonymized client contracts, or audit documents) to substantiate claimed outcomes.",
        "trigger": "Consultant navigates to the 'Evidence & Verification' tab in the Creation Studio.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Case study draft is created.",
            "2. External accounts (e.g. GitHub) connected if repository proof is used."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Attach verifiable evidence and execution proofs", "flow": "", "info": "Evidence Attachment"},
            {"step": "1", "action": "Consultant selects evidence type (GitHub Commit Link, Live Domain URL, PDF Audit Memo, Client Co-Sign)", "flow": "<-", "info": "Evidence Type"},
            {"step": "2", "action": "Consultant provides proof URL or uploads sanitized document", "flow": "<-", "info": "Proof URL / Uploaded Asset"},
            {"step": "3", "action": "System queries external API (e.g., GitHub API to verify commit hash, author, and timestamp)", "flow": "<-", "info": "External Proof API response"},
            {"step": "4", "action": "System generates cryptographic SHA-256 hash of the evidence snapshot", "flow": "->", "info": "Evidence SHA-256 Digest"},
            {"step": "5", "action": "System badges the evidence item as 'Verified Execution Proof'", "flow": "->", "info": "Verified Evidence Badge"},
            {"step": "6", "action": "Consultant links specific claims in the case study text to the attached proof badges", "flow": "<-", "info": "Claim-to-Proof link mapping"}
        ],
        "alternatives": [
            {
                "id": "6.1",
                "title": "Client Co-Sign verification request",
                "steps": [
                    {"step": "1", "action": "Consultant enters verified corporate client email address for co-attestation", "flow": "<-", "info": "Client corporate email"},
                    {"step": "2a", "action": "System dispatches magic verification token to client stakeholder", "flow": "->", "info": "Client attestation token"},
                    {"step": "3a", "action": "Evidence displays 'Pending Client Attestation' until authenticated signature received", "flow": "->", "info": "Pending badge state"}
                ]
            }
        ],
        "postconditions": [
            "1. Evidence records linked to the case study entity with immutable timestamps.",
            "2. Creator Authority Score potential boosts calculated for publication."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Invalid or broken external URL / 404 commit link",
                "steps": [
                    "1. System displays validation error: 'Unable to reach repository commit. Please verify repository is public or authorize private read access.'",
                    "2. System rejects evidence submission until resolved."
                ]
            }
        ],
        "inputs": [
            ("Proof URLs, GitHub credentials, PDF files", "Consultant Input"),
            ("GitHub / GitLab API verification response", "External Repository Rails")
        ],
        "outputs": [
            ("Cryptographic Evidence Record", "Evidence Vault Datastore"),
            ("Verified Proof Badges", "Case Study View")
        ],
        "fr_correlation": ["FR-006 (Evidence Verification & Attestation)", "FR-017 (CAS Credibility Metrics)"],
        "testing_mapping": {
            "positive_tests": ["TC-06-01: Verify GitHub commit hash query confirms author match and displays commit date."],
            "boundary_tests": ["TC-06-02: Test upload of 25MB encrypted PDF audit memo with automatic metadata stripping."],
            "exception_tests": ["TC-06-03: Verify handling of rate-limited external APIs with exponential backoff."]
        }
    },
    {
        "id": "UC-07",
        "name": "Attach Conversion Anchor Call-to-Action",
        "priority": "High",
        "actor": "Consultant / Specialist Creator",
        "description": "The Consultant configures a native conversion anchor at the bottom of the case study. This hook enables readers to immediately take commercial action (e.g., 'Book 30-Min Strategy Call - KES 10,000', 'Request Architecture Audit SOW', or 'Hire via Milestone Escrow').",
        "trigger": "Consultant completes case study content and navigates to the 'Conversion Hook' step.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Consultant has configured billing rates or calendar availability.",
            "2. Case study content meets publication minimums."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Configure native business conversion anchor", "flow": "", "info": "Anchor Setup"},
            {"step": "1", "action": "Consultant selects conversion anchor type (Live Advisory Session, Fixed-Price Audit, SOW Proposal Inquiry)", "flow": "<-", "info": "Anchor Type"},
            {"step": "2", "action": "Consultant defines price in KES / USD and service duration (e.g., KES 15,000 for 45 mins)", "flow": "<-", "info": "Pricing & Duration parameters"},
            {"step": "3", "action": "Consultant specifies intake form questionnaire required from client before booking", "flow": "<-", "info": "Intake questionnaire fields"},
            {"step": "4", "action": "System validates pricing complies with platform minimums and Kenyan tax rules", "flow": "->", "info": "Pricing validation status"},
            {"step": "5", "action": "System embeds sticky conversion drawer at base of case study deck", "flow": "->", "info": "Configured Conversion Anchor"}
        ],
        "alternatives": [
            {
                "id": "7.1",
                "title": "Consultant links anchor to custom Enterprise RFP inquiry",
                "steps": [
                    {"step": "1", "action": "Consultant selects 'Custom SOW Inquiry' without fixed pricing", "flow": "<-", "info": "RFP option flag"},
                    {"step": "2a", "action": "System configures RFP submission wizard with NDA checkbox and budget bracket dropdown", "flow": "->", "info": "RFP Wizard setup"}
                ]
            }
        ],
        "postconditions": [
            "1. Case study is equipped with actionable commercial trigger ready for publishing.",
            "2. Anchor configuration stored in case study metadata."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Pricing below statutory or platform minimum",
                "steps": [
                    "1. System displays warning: 'Advisory consultation price cannot be lower than KES 2,500.'",
                    "2. Consultant adjusts price to continue."
                ]
            }
        ],
        "inputs": [
            ("Anchor type, fee amount, intake questions", "Consultant Input")
        ],
        "outputs": [
            ("Conversion Anchor Configuration", "Case Study Datastore"),
            ("Rendered Sticky CTA Drawer", "Reader Interface")
        ],
        "fr_correlation": ["FR-007 (Conversion Anchor Infrastructure)", "FR-009 (Consultation Scheduling)"],
        "testing_mapping": {
            "positive_tests": ["TC-07-01: Verify conversion CTA persists and renders correctly across mobile viewport."],
            "boundary_tests": ["TC-07-02: Verify multi-currency price conversion (KES to USD/EUR) based on daily CBK rates."],
            "exception_tests": ["TC-07-03: Verify attempt to publish without active calendar fails with helpful guidance."]
        }
    },
    {
        "id": "UC-08",
        "name": "Verify Professional Identity & Credentials",
        "priority": "High",
        "actor": "Consultant / Specialist Creator",
        "description": "The Consultant submits national identification documents and regulatory professional licenses (e.g., Law Society of Kenya - LSK, ICPAK, Engineers Board of Kenya - EBK) for formal verification against statutory registries to earn verified platform authority tiers.",
        "trigger": "Consultant initiates verification in the 'Trust & Authority' section of settings.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Consultant is logged into KenyaConsult.",
            "2. Government and professional API gateways (IPRS/eCitizen, LSK, ICPAK, EBK) are reachable or queueable."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Verify identity and professional board credentials", "flow": "", "info": "Verification Initiation"},
            {"step": "1", "action": "Consultant selects verification category (National ID / Passport, Professional Body License, Tax PIN)", "flow": "<-", "info": "Verification Category"},
            {"step": "2", "action": "Consultant enters National ID Number, KRA PIN, and Professional Practicing Certificate Number", "flow": "<-", "info": "ID & Registration Credentials"},
            {"step": "3", "action": "Consultant uploads scan of Practicing Certificate and national document", "flow": "<-", "info": "Scanned Document files"},
            {"step": "4", "action": "System queries government IPRS / KRA API to validate ID and tax compliance status", "flow": "<-", "info": "IPRS / KRA API validation response"},
            {"step": "5", "action": "System queries professional board registry (e.g. LSK Advocate Roll, ICPAK Member Register)", "flow": "<-", "info": "Board Registry verification data"},
            {"step": "6", "action": "System confirms match of full name, registration number, and active standing", "flow": "->", "info": "Match Confirmation status"},
            {"step": "7", "action": "System awards 'Verified Specialist' badge and upgrades CAS tier from Tier 1 to Tier 3", "flow": "->", "info": "Awarded Badge & CAS multiplier"},
            {"step": "8", "action": "System logs cryptographic verification timestamp in the immutable audit ledger", "flow": "->", "info": "Audit Ledger entry"}
        ],
        "alternatives": [
            {
                "id": "8.1",
                "title": "Automated registry API is offline or requires manual review (branch at step 5)",
                "steps": [
                    {"step": "1", "action": "System detects board registry timeout or manual verification requirement", "flow": "<-", "info": "Registry API timeout"},
                    {"step": "2a", "action": "System queues application into Compliance Officer review queue (UC-20)", "flow": "->", "info": "Manual Review Queue entry"},
                    {"step": "3a", "action": "System notifies consultant: 'Credentials submitted. Manual review completes within 24 hours.'", "flow": "->", "info": "Pending review notice"}
                ]
            }
        ],
        "postconditions": [
            "1. Consultant profile displays verified credentials seals.",
            "2. Consultant CAS score increased by 40% authoritative weighting.",
            "3. Sensitive documents securely encrypted with AES-256 and PII redacted from public views."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Name mismatch between National ID and Professional Board License (occurs at step 6)",
                "steps": [
                    "1. System flags discrepancy: 'Name on LSK License does not match National ID. Please upload official deed poll or contact support.'",
                    "2. Application flagged for manual verification officer."
                ]
            }
        ],
        "inputs": [
            ("National ID, KRA PIN, Board Registration #, Certificate Scans", "Consultant Input"),
            ("Registry API verification payloads", "IPRS / KRA / LSK / ICPAK / EBK APIs")
        ],
        "outputs": [
            ("Verified Authority Badges", "Consultant Profile UI"),
            ("Upgraded CAS Multiplier", "Recommendation Engine"),
            ("Verification Audit Record", "Compliance Vault")
        ],
        "fr_correlation": ["FR-008 (Identity & Credential Verification)", "FR-017 (CAS Tiering)", "FR-020 (Compliance & Moderation)"],
        "testing_mapping": {
            "positive_tests": ["TC-08-01: Verify valid ICPAK practicing member number updates profile badge in < 5 seconds."],
            "boundary_tests": ["TC-08-02: Test high-resolution PDF upload (15MB) with automatic EXIF/PII sanitization."],
            "exception_tests": ["TC-08-03: Verify expired practicing certificate triggers alert and rejects tier upgrade."]
        }
    },
    {
        "id": "UC-09",
        "name": "Book In-App Advisory Consultation",
        "priority": "High",
        "actor": "Client / Enterprise Buyer",
        "description": "The Client books a 1-on-1 advisory consultation with a verified specialist directly from a case study or profile. The system resolves real-time calendar availability, captures pre-intake briefing questions, and reserves the slot pending payment.",
        "trigger": "Client clicks 'Book Advisory Consultation' anchor on a case study or profile Bento card.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Client is authenticated (or completes quick SMS OTP verification).",
            "2. Consultant has synchronized external calendar (Google Calendar / Outlook)."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Schedule advisory consultation and reserve slot", "flow": "", "info": "Booking Initialization"},
            {"step": "1", "action": "Client clicks 'Book Consultation' anchor", "flow": "<-", "info": "Booking CTA Click"},
            {"step": "2", "action": "System queries Google/Outlook calendar API and presents live interactive availability calendar", "flow": "->", "info": "Live available time slots"},
            {"step": "3", "action": "Client selects preferred date, time slot, and session duration (e.g., Oct 24, 2:00 PM - 3:00 PM EAT)", "flow": "<-", "info": "Selected Date & Slot ID"},
            {"step": "4", "action": "System places a 15-minute temporary soft lock on the chosen calendar slot", "flow": "->", "info": "15-minute slot lock"},
            {"step": "5", "action": "System presents structured intake form: [Consultation Objective, Tech Stack / Legal Domain, Uploaded Docs]", "flow": "->", "info": "Intake questionnaire form"},
            {"step": "6", "action": "Client completes questionnaire and submits details", "flow": "<-", "info": "Client intake responses & attachments"},
            {"step": "7", "action": "System validates responses and displays payment selection drawer (triggers UC-10 or UC-11)", "flow": "->", "info": "Booking Summary & Fee invoice"}
        ],
        "alternatives": [
            {
                "id": "9.1",
                "title": "Selected slot is claimed by another user before lock (race condition)",
                "steps": [
                    {"step": "1", "action": "System detects simultaneous booking conflict during lock", "flow": "<-", "info": "Calendar conflict notice"},
                    {"step": "2a", "action": "System alerts client: 'Slot was just booked. Showing nearest open alternatives.'", "flow": "->", "info": "Next available slot options"},
                    {"step": "3a", "action": "Client picks alternative slot and resumes Normal Course at step 4", "flow": "<-", "info": "Alternative slot pick"}
                ]
            }
        ],
        "postconditions": [
            "1. Booking entity created with status 'PENDING_PAYMENT'.",
            "2. Temporary 15-minute reservation held in Redis slot coordinator.",
            "3. Client forwarded to payment checkout."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Client abandons checkout / 15-minute timer expires",
                "steps": [
                    "1. Redis timer expires without confirmed payment.",
                    "2. System automatically releases calendar slot lock and marks booking 'ABANDONED'.",
                    "3. Slot becomes instantly available again to the public."
                ]
            }
        ],
        "inputs": [
            ("Slot selection, intake form text, attachments", "Client Input"),
            ("Calendar availability schedule", "Google Calendar / Outlook API")
        ],
        "outputs": [
            ("Temporary Calendar Slot Lock", "Redis Coordination Layer"),
            ("Pending Booking Record", "Booking Database"),
            ("Fee Summary Invoice", "Client Display")
        ],
        "fr_correlation": ["FR-009 (Native Booking Engine)", "FR-010 (M-Pesa STK Integration)", "FR-011 (Cross-Border Billing)"],
        "testing_mapping": {
            "positive_tests": ["TC-09-01: Verify selected slot acquires Redis lock and prevents concurrent double booking."],
            "boundary_tests": ["TC-09-02: Test booking across time zones (e.g. Client in London BST booking Nairobi EAT)."],
            "exception_tests": ["TC-09-03: Verify slot lock automatically expires after exactly 900 seconds of inactivity."]
        }
    },
    {
        "id": "UC-10",
        "name": "Process Payment via M-Pesa STK Push",
        "priority": "High",
        "actor": "Client / Enterprise Buyer",
        "description": "The Client pays for a consultation booking or milestone escrow contract using M-Pesa mobile money. The platform triggers an instant Safaricom Daraja STK Push to the user's mobile device, verifies PIN authorization, and locks funds in escrow.",
        "trigger": "Client selects 'M-Pesa' as payment method on the checkout drawer and clicks 'Pay Now'.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Booking or escrow contract is in 'PENDING_PAYMENT' state.",
            "2. Safaricom Daraja API gateway is operational.",
            "3. Client has an active Safaricom line with sufficient balance."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Execute M-Pesa mobile payment via Daraja STK Push", "flow": "", "info": "Payment Execution"},
            {"step": "1", "action": "Client enters Safaricom mobile phone number (e.g. 0712345678) and confirms fee amount", "flow": "<-", "info": "Phone number & Amount"},
            {"step": "2", "action": "System sanitizes phone number into international format (+254712345678)", "flow": "->", "info": "Normalized phone number"},
            {"step": "3", "action": "System issues Lipa Na M-Pesa Online STK Push request to Safaricom Daraja API", "flow": "->", "info": "Daraja STK payload"},
            {"step": "4", "action": "Client's mobile handset receives on-screen prompt: 'Do you want to pay KES 10,000 to KenyaConsult?'", "flow": "->", "info": "Safaricom USSD / SIM Prompt"},
            {"step": "5", "action": "Client inputs secret M-Pesa PIN on handset and submits", "flow": "<-", "info": "Encrypted PIN submission"},
            {"step": "6", "action": "Safaricom validates funds and delivers asynchronous Callback to platform webhook URL", "flow": "<-", "info": "Daraja Callback JSON payload"},
            {"step": "7", "action": "System verifies callback signature, transaction code (e.g. 'RJK894KL9'), and exact amount paid", "flow": "<-", "info": "M-Pesa Transaction Code"},
            {"step": "8", "action": "System transitions booking status from 'PENDING_PAYMENT' to 'CONFIRMED_ESCROW_LOCKED'", "flow": "->", "info": "Updated Booking Entity"},
            {"step": "9", "action": "System dispatches instant SMS and email receipt with encrypted calendar invite to both parties", "flow": "->", "info": "Receipt & Calendar Invite"}
        ],
        "alternatives": [
            {
                "id": "10.1",
                "title": "Client cancels prompt on handset or enters incorrect PIN",
                "steps": [
                    {"step": "1", "action": "Safaricom delivers failure callback with ResultCode 1032 ('Request cancelled by user')", "flow": "<-", "info": "Cancellation Callback"},
                    {"step": "2a", "action": "System updates checkout screen: 'Payment cancelled on handset. Try again or choose Card payment.'", "flow": "->", "info": "Retry Prompt UI"},
                    {"step": "3a", "action": "Client taps 'Retry M-Pesa' or selects Card", "flow": "<-", "info": "User Retry Choice"}
                ]
            },
            {
                "id": "10.2",
                "title": "Insufficient balance on M-Pesa account",
                "steps": [
                    {"step": "1", "action": "Safaricom callback indicates ResultCode 1 ('Insufficient funds')", "flow": "<-", "info": "Insufficient Funds Code"},
                    {"step": "2a", "action": "System notifies client to top up M-Pesa or switch payment methods", "flow": "->", "info": "Insufficient funds alert"}
                ]
            }
        ],
        "postconditions": [
            "1. Transaction recorded in KenyaConsult double-entry financial ledger.",
            "2. Funds deposited into platform trust escrow account.",
            "3. Calendar booking finalized and WebRTC room generated (triggers UC-12)."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Daraja webhook callback delayed or network timeout (>60 seconds)",
                "steps": [
                    "1. Platform initiates active Daraja Transaction Status Query polling endpoint.",
                    "2. Upon receiving positive query response, platform reconciles transaction and confirms booking.",
                    "3. If query times out after 3 minutes, client is prompted to enter M-Pesa SMS transaction code for automated manual matching."
                ]
            }
        ],
        "inputs": [
            ("Phone number & Consultation Fee", "Client Checkout Form"),
            ("Daraja Callback JSON payload", "Safaricom Payment Gateway")
        ],
        "outputs": [
            ("STK Push Request", "Safaricom Daraja API"),
            ("Confirmed Booking & Escrow Receipt", "Client & Consultant"),
            ("Financial Ledger Record", "Platform Accounting System")
        ],
        "fr_correlation": ["FR-010 (M-Pesa STK Push Integration)", "FR-013 (Escrow Ledger Management)", "FR-022 (Tax & eTIMS Compliance)"],
        "testing_mapping": {
            "positive_tests": ["TC-10-01: Verify successful Daraja callback (ResultCode 0) updates booking to CONFIRMED within 3 seconds."],
            "boundary_tests": ["TC-10-02: Test maximum single transaction limit (KES 250,000 per CBK/Safaricom limits)."],
            "exception_tests": ["TC-10-03: Verify idempotency—duplicate callbacks with same M-Pesa code do not create duplicate ledger entries."]
        }
    },
    {
        "id": "UC-11",
        "name": "Process Cross-Border Card Payment",
        "priority": "Medium",
        "actor": "Client / Enterprise Buyer (Diaspora / International)",
        "description": "The Client pays for services using international credit/debit cards (Visa, Mastercard, American Express). The payment is processed via 3D Secure 2.0 with automated currency conversion to Kenyan Shillings (KES).",
        "trigger": "Client selects 'Credit / Debit Card' on checkout drawer.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Booking or escrow milestone is in 'PENDING_PAYMENT'.",
            "2. International payment gateway (Paystack / Flutterwave / Stripe) is operational."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Process card payment with 3D Secure verification", "flow": "", "info": "Card Processing"},
            {"step": "1", "action": "Client enters Cardholder Name, 16-digit Card Number, Expiry, and CVV", "flow": "<-", "info": "Card credentials (tokenized)"},
            {"step": "2", "action": "Client-side library tokenizes card data directly to PCI-DSS Level 1 gateway", "flow": "->", "info": "Card Token"},
            {"step": "3", "action": "Gateway initiates 3D Secure challenge (OTP / Bank App authentication)", "flow": "->", "info": "3DS Challenge Modal"},
            {"step": "4", "action": "Client confirms challenge with issuing bank", "flow": "<-", "info": "3DS Authentication"},
            {"step": "5", "action": "Gateway executes fund capture and emits successful charge webhook to platform", "flow": "<-", "info": "Charge Success Webhook"},
            {"step": "6", "action": "System locks equivalent KES amount in milestone escrow and generates tax invoice", "flow": "->", "info": "Escrow confirmation & invoice"}
        ],
        "alternatives": [
            {
                "id": "11.1",
                "title": "Card declined (insufficient funds, fraud block, or expired card)",
                "steps": [
                    {"step": "1", "action": "Gateway returns decline error code (e.g. 'card_declined', 'insufficient_funds')", "flow": "<-", "info": "Decline error payload"},
                    {"step": "2a", "action": "System displays user-friendly bank decline explanation and prompts for alternative card", "flow": "->", "info": "Decline UI notification"}
                ]
            }
        ],
        "postconditions": [
            "1. Funds locked into escrow vault.",
            "2. Booking status transitions to 'CONFIRMED'."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "3D Secure authentication timeout or failure",
                "steps": [
                    "1. Gateway voids pending authorization.",
                    "2. Booking remains pending payment with slot preserved for 5 minutes."
                ]
            }
        ],
        "inputs": [
            ("Tokenized card data", "Client Browser"),
            ("Charge success webhook payload", "Paystack / Flutterwave Gateway")
        ],
        "outputs": [
            ("Card Charge Token", "Payment Gateway API"),
            ("Confirmed Booking Record", "Booking Database")
        ],
        "fr_correlation": ["FR-011 (Cross-Border Multi-Currency Billing)", "FR-013 (Escrow Ledger Management)"],
        "testing_mapping": {
            "positive_tests": ["TC-11-01: Verify 3DS 2.0 flow successfully executes and records exchange rate at transaction time."],
            "boundary_tests": ["TC-11-02: Test high-value international transaction ($5,000 USD) with fraud screening."],
            "exception_tests": ["TC-11-03: Verify zero card details (PAN/CVV) touch platform application servers (PCI-DSS audit compliance)."]
        }
    },
    {
        "id": "UC-12",
        "name": "Conduct Secure Live Consultation",
        "priority": "High",
        "actor": "Client & Consultant",
        "description": "At the scheduled time, the Client and Consultant join an encrypted, zero-friction in-browser WebRTC video consultation room. The room provides screen sharing, collaborative note-taking, and automatically logs session duration and completion.",
        "trigger": "Scheduled appointment time arrives or either party clicks 'Join Consultation Room'.",
        "type_external": True,
        "type_temporal": True,
        "preconditions": [
            "1. Booking status is 'CONFIRMED_ESCROW_LOCKED'.",
            "2. Both parties have verified access tokens.",
            "3. Client and consultant devices support WebRTC."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Conduct live video consultation and record session artifacts", "flow": "", "info": "Live Consultation"},
            {"step": "1", "action": "Client and Consultant access meeting URL within 10 minutes of scheduled start", "flow": "<-", "info": "Room Access Token"},
            {"step": "2", "action": "System verifies meeting validity, checks participant credentials, and opens WebRTC media room", "flow": "->", "info": "Encrypted WebRTC Channel"},
            {"step": "3", "action": "Both participants join with mutual audio/video streams established", "flow": "->", "info": "Live A/V Streams"},
            {"step": "4", "action": "Participants collaborate using in-app screen sharing and shared action item scratchpad", "flow": "<-", "info": "Collaborative Notes & Action Items"},
            {"step": "5", "action": "System records real-time call telemetry (start timestamp, end timestamp, connection quality)", "flow": "->", "info": "Call Telemetry Record"},
            {"step": "6", "action": "Session concludes; either participant clicks 'End Session'", "flow": "<-", "info": "Session End Command"},
            {"step": "7", "action": "System compiles meeting action summary and sends copy to both parties", "flow": "->", "info": "Meeting Summary & Action Items"},
            {"step": "8", "action": "System transitions booking to 'SESSION_COMPLETED_PENDING_REVIEW'", "flow": "->", "info": "Updated Booking Entity"}
        ],
        "alternatives": [
            {
                "id": "12.1",
                "title": "Either party experiences connection drop during call (network reconnection)",
                "steps": [
                    {"step": "1", "action": "WebRTC peer connection drops due to unstable internet", "flow": "<-", "info": "Connection Drop event"},
                    {"step": "2a", "action": "System maintains room open for 15-minute grace period and displays reconnection banner", "flow": "->", "info": "Reconnection Waiting Room"},
                    {"step": "3a", "action": "Disconnected party rejoins and session resumes", "flow": "<-", "info": "Reconnection token"}
                ]
            },
            {
                "id": "12.2",
                "title": "Consultant or Client is a no-show (15 minutes elapsed)",
                "steps": [
                    {"step": "1", "action": "System timer reaches 15 minutes past start with only one party present", "flow": "<-", "info": "No-Show timer trigger"},
                    {"step": "2a", "action": "System logs verified no-show timestamp", "flow": "->", "info": "No-Show Event Record"},
                    {"step": "3a", "action": "If Consultant no-show: Full refund initiated to Client. If Client no-show: 50% cancellation fee paid to Consultant.", "flow": "->", "info": "Escrow Policy Action"}
                ]
            }
        ],
        "postconditions": [
            "1. Meeting completion timestamp permanently logged.",
            "2. Both parties prompted for private session feedback and ratings.",
            "3. Escrow release window initiates."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Browser denies camera or microphone permissions",
                "steps": [
                    "1. System displays modal with illustrated browser permission fix steps.",
                    "2. System provides one-click option to switch to audio-only mode."
                ]
            }
        ],
        "inputs": [
            ("Meeting room access tokens, audio/video streams", "Browser WebRTC API"),
            ("In-session notes and screen share events", "Participants")
        ],
        "outputs": [
            ("Encrypted WebRTC Audio/Video Session", "Participant Browsers"),
            ("Action Items & Meeting Summary PDF", "Client & Consultant Email"),
            ("Session Completion Telemetry", "Escrow Ledger")
        ],
        "fr_correlation": ["FR-012 (WebRTC Video Infrastructure)", "FR-015 (Escrow Release Engine)"],
        "testing_mapping": {
            "positive_tests": ["TC-12-01: Verify peer-to-peer connection establishes under 2 seconds on standard fiber/4G."],
            "boundary_tests": ["TC-12-02: Test automated no-show policy triggering at exactly 15 minutes 00 seconds."],
            "exception_tests": ["TC-12-03: Verify end-to-end media encryption (DTLS-SRTP) prevents unauthorized eavesdropping."]
        }
    },
    {
        "id": "UC-13",
        "name": "Fund Milestone Escrow Contract",
        "priority": "High",
        "actor": "Client / Enterprise Buyer",
        "description": "The Client locks project capital into the platform's multi-stage escrow vault for a phased B2B consulting engagement. Funds are held in trust according to a formal Statement of Work (SOW) with defined milestone release conditions.",
        "trigger": "Client reviews and accepts a consultant's project proposal / SOW.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Formal SOW proposal created with at least one milestone and agreed deliverables.",
            "2. Both Client and Consultant have agreed to platform Escrow Terms."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Fund and lock milestone escrow contract", "flow": "", "info": "Escrow Funding"},
            {"step": "1", "action": "Client reviews proposal: [Milestones 1..N, Due Dates, Deliverables, Acceptance Criteria, Amounts]", "flow": "<-", "info": "SOW Proposal Data"},
            {"step": "2", "action": "Client chooses to fund either Milestone 1 or Full Contract up front", "flow": "<-", "info": "Funding Scope selection"},
            {"step": "3", "action": "Client selects payment rail (M-Pesa, Card, Bank Wire / RTGS for >KES 500,000)", "flow": "<-", "info": "Selected Payment Method"},
            {"step": "4", "action": "System processes transaction through selected gateway", "flow": "->", "info": "Payment Gateway Payload"},
            {"step": "5", "action": "System confirms receipt and registers funds in immutable Escrow Ledger under contract UUID", "flow": "->", "info": "Escrow Ledger Record"},
            {"step": "6", "action": "System emits contract state event: 'ESCROW_FUNDED_ACTIVE'", "flow": "->", "info": "Contract State Event"},
            {"step": "7", "action": "System notifies Consultant that project is funded and authorized to begin work", "flow": "->", "info": "Work Authorization Notice"}
        ],
        "alternatives": [
            {
                "id": "13.1",
                "title": "Corporate Client pays via Bank Transfer / RTGS invoice",
                "steps": [
                    {"step": "1", "action": "Client selects 'Bank Wire / RTGS Invoice' option", "flow": "<-", "info": "RTGS selection"},
                    {"step": "2a", "action": "System issues pro-forma invoice with unique Virtual Account Number (VAN) and reference code", "flow": "->", "info": "Pro-Forma Invoice with VAN"},
                    {"step": "3a", "action": "System awaits automated commercial bank reconciliation webhook", "flow": "<-", "info": "Bank settlement confirmation"},
                    {"step": "4a", "action": "System locks escrow upon settlement confirmation and notifies parties", "flow": "->", "info": "Funded notification"}
                ]
            }
        ],
        "postconditions": [
            "1. Escrow contract active with funds securely segregated in partner trust bank.",
            "2. Consultant protected against client default before commencing work."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Bank transfer amount mismatch (e.g. less than milestone sum due to wire fees)",
                "steps": [
                    "1. System flags underpayment in escrow ledger.",
                    "2. System generates balance top-up request to client before milestone activation."
                ]
            }
        ],
        "inputs": [
            ("Proposal acceptance & Payment details", "Client Input"),
            ("Bank / Gateway settlement notifications", "Fintech Rails")
        ],
        "outputs": [
            ("Escrow Ledger Entry", "Platform Financial Ledger"),
            ("Work Authorization Notice", "Consultant Dashboard"),
            ("Tax Pro-Forma Invoice", "Client Organization")
        ],
        "fr_correlation": ["FR-013 (Milestone Escrow Architecture)", "FR-010 (M-Pesa STK Push)", "FR-011 (Card Rails)"],
        "testing_mapping": {
            "positive_tests": ["TC-13-01: Verify successful funding transitions milestone status from DRAFT to FUNDED."],
            "boundary_tests": ["TC-13-02: Test high-value escrow contract (KES 2,000,000) funded via multi-tranche RTGS."],
            "exception_tests": ["TC-13-03: Verify funds remain strictly untouched and unreleased until explicit approval or adjudication."]
        }
    },
    {
        "id": "UC-14",
        "name": "Submit Project Milestone Deliverable",
        "priority": "High",
        "actor": "Consultant / Specialist Creator",
        "description": "The Consultant uploads finished project deliverables (code, documents, blueprints, reports) for an active escrow milestone. The system computes a cryptographic SHA-256 fingerprint, timestamps the submission, and triggers the client's 72-hour review window.",
        "trigger": "Consultant clicks 'Submit Deliverable' on an active milestone in project dashboard.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Project contract status is 'ESCROW_FUNDED_ACTIVE'.",
            "2. Milestone status is 'IN_PROGRESS'."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Submit milestone deliverable with cryptographic fingerprint", "flow": "", "info": "Deliverable Submission"},
            {"step": "1", "action": "Consultant navigates to active milestone and clicks 'Submit Deliverable'", "flow": "<-", "info": "Submit Trigger"},
            {"step": "2", "action": "Consultant provides completion notes, live links (GitHub PR, staging URL), and file uploads", "flow": "<-", "info": "Deliverable Files & Links"},
            {"step": "3", "action": "System uploads files to encrypted cloud storage and generates SHA-256 cryptographic hash of all files", "flow": "->", "info": "SHA-256 Artifact Digests"},
            {"step": "4", "action": "System stores immutable delivery record with server timestamp", "flow": "->", "info": "Delivery Audit Record"},
            {"step": "5", "action": "System transitions milestone status to 'SUBMITTED_UNDER_REVIEW'", "flow": "->", "info": "Milestone State Update"},
            {"step": "6", "action": "System starts 72-hour inspection countdown timer", "flow": "->", "info": "72-Hour Inspection Timer"},
            {"step": "7", "action": "System dispatches instant notification and review link to Client", "flow": "->", "info": "Client Review Notification"}
        ],
        "alternatives": [
            {
                "id": "14.1",
                "title": "Consultant uploads revisions following client feedback",
                "steps": [
                    {"step": "1", "action": "Consultant submits updated assets addressing requested changes", "flow": "<-", "info": "Revised assets"},
                    {"step": "2a", "action": "System creates new deliverable revision (v2), resets review countdown, and preserves v1 for dispute audit", "flow": "->", "info": "Revision versioning"}
                ]
            }
        ],
        "postconditions": [
            "1. Deliverable assets secured in tamper-proof repository.",
            "2. 72-hour auto-approval clock running."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Uploaded deliverable contains infected or prohibited file types (.exe, malware)",
                "steps": [
                    "1. Malware scanner isolates uploaded artifact in sandbox.",
                    "2. System rejects upload with security alert: 'Prohibited file type detected.'",
                    "3. Consultant prompted to upload clean archive."
                ]
            }
        ],
        "inputs": [
            ("Deliverable files, PR links, completion summary", "Consultant Input")
        ],
        "outputs": [
            ("Encrypted Artifacts & SHA-256 Hashes", "Cloud Object Storage"),
            ("72-Hour Review Timer Event", "Task Scheduler / Celery"),
            ("Client Review Notification", "Client Email & In-App")
        ],
        "fr_correlation": ["FR-014 (Cryptographic Deliverable Proofs)", "FR-015 (Inspection Window Timer)"],
        "testing_mapping": {
            "positive_tests": ["TC-14-01: Verify SHA-256 hash matches exact byte content of uploaded deliverable archive."],
            "boundary_tests": ["TC-14-02: Test submission right at the exact milestone deadline (23:59:59)."],
            "exception_tests": ["TC-14-03: Verify virus scanner quarantines test EICAR file without affecting platform stability."]
        }
    },
    {
        "id": "UC-15",
        "name": "Review & Approve Escrow Milestone",
        "priority": "High",
        "actor": "Client / Enterprise Buyer",
        "description": "The Client reviews the consultant's submitted deliverable. Upon satisfaction, the client clicks 'Approve & Release Funds'. The system automatically calculates platform take rate (5-8%), generates a KRA eTIMS tax invoice, releases net payout to the consultant via M-Pesa B2C or bank transfer, and updates project status.",
        "trigger": "Client reviews deliverable and clicks 'Approve Milestone'.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Milestone status is 'SUBMITTED_UNDER_REVIEW'.",
            "2. Funds are currently locked in escrow."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Approve deliverable and disburse escrow payout", "flow": "", "info": "Milestone Approval"},
            {"step": "1", "action": "Client accesses deliverable review dashboard and verifies submitted deliverables against SOW criteria", "flow": "<-", "info": "Inspection Action"},
            {"step": "2", "action": "Client clicks 'Approve Milestone & Release Funds'", "flow": "<-", "info": "Approval Command"},
            {"step": "3", "action": "System displays release confirmation modal with breakdown: [Milestone Total | Platform Commission (7%) | Withholding Tax | Net Consultant Payout]", "flow": "->", "info": "Fee Breakdown Modal"},
            {"step": "4", "action": "Client enters 2FA code / biometric confirmation", "flow": "<-", "info": "Client 2FA Token"},
            {"step": "5", "action": "System executes financial settlement in double-entry ledger", "flow": "->", "info": "Ledger Settlement Record"},
            {"step": "6", "action": "System transmits electronic invoice to KRA eTIMS API and attaches official QR code", "flow": "->", "info": "KRA eTIMS Invoice Submission"},
            {"step": "7", "action": "System triggers automated B2C payout to consultant via M-Pesa B2C or RTGS", "flow": "->", "info": "B2C Payout Instruction"},
            {"step": "8", "action": "Consultant receives instant payout notification and funds in mobile wallet", "flow": "->", "info": "Payout Notification"},
            {"step": "9", "action": "System transitions milestone status to 'COMPLETED_RELEASED'", "flow": "->", "info": "Milestone State Update"}
        ],
        "alternatives": [
            {
                "id": "15.1",
                "title": "72-hour review timer elapses without client action (Auto-Approval)",
                "steps": [
                    {"step": "1", "action": "72-hour inspection countdown reaches 0 with no client dispute or rejection filed", "flow": "<-", "info": "Timer Expiry Trigger"},
                    {"step": "2a", "action": "System automatically invokes step 5 through step 9 of Normal Course under contractual auto-approval policy", "flow": "->", "info": "Auto-Approval Execution"},
                    {"step": "3a", "action": "System sends notification to client: 'Milestone auto-approved per platform terms.'", "flow": "->", "info": "Auto-Approval notice"}
                ]
            },
            {
                "id": "15.2",
                "title": "Client requests revisions (branch at step 2)",
                "steps": [
                    {"step": "1", "action": "Client clicks 'Request Revisions' and inputs specific unfulfilled requirements", "flow": "<-", "info": "Revision Feedback Notes"},
                    {"step": "2a", "action": "Milestone status transitions to 'REVISIONS_REQUESTED'", "flow": "->", "info": "Revision Status"},
                    {"step": "3a", "action": "Consultant notified to submit updated deliverable (UC-14)", "flow": "->", "info": "Revision Task Notice"}
                ]
            }
        ],
        "postconditions": [
            "1. Net funds disbursed to consultant.",
            "2. Platform commission credited to KenyaConsult operational account.",
            "3. KRA eTIMS tax invoice generated with cryptographic QR code.",
            "4. Consultant's CAS score updated with successful milestone completion points."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "B2C M-Pesa payout API failure (e.g. utility wallet underfunded or telco timeout)",
                "steps": [
                    "1. System flags payout as 'PENDING_MANUAL_DISBURSEMENT' without losing ledger state.",
                    "2. Finance team alerted via PagerDuty to replenish corporate B2C account.",
                    "3. Automated retry worker executes payout within 30 minutes."
                ]
            }
        ],
        "inputs": [
            ("Client approval confirmation & 2FA token", "Client Input"),
            ("Milestone contract financial parameters", "Escrow Ledger")
        ],
        "outputs": [
            ("B2C Mobile Payout / Bank Wire", "Consultant Mobile Wallet"),
            ("KRA eTIMS Electronic Invoice", "KRA Tax Registry & Client"),
            ("Completed Ledger Entry", "Platform Financial Ledger")
        ],
        "fr_correlation": ["FR-015 (Escrow Release Engine)", "FR-016 (Dispute Handling)", "FR-022 (Tax & eTIMS Compliance)"],
        "testing_mapping": {
            "positive_tests": ["TC-15-01: Verify fund release accurately applies 7% commission and credits net balance."],
            "boundary_tests": ["TC-15-02: Test automatic auto-approval execution at exactly 72 hours 00 minutes 01 seconds."],
            "exception_tests": ["TC-15-03: Verify transaction rollback if ledger database fails during settlement step."]
        }
    },
    {
        "id": "UC-16",
        "name": "Initiate Escrow Dispute & Mediation",
        "priority": "Medium",
        "actor": "Client or Consultant",
        "description": "Either party freezes automated escrow releases when an unresolvable breach of contract, non-delivery, or scope disagreement occurs. The dispute locks remaining escrow funds in vault and summons a Platform Escrow Mediator for formal adjudication.",
        "trigger": "User clicks 'Raise Dispute & Request Mediation' within milestone dashboard.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Milestone is in 'SUBMITTED_UNDER_REVIEW' or 'REVISIONS_REQUESTED'.",
            "2. At least one round of mutual revision feedback was attempted."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Freeze escrow and file dispute claim", "flow": "", "info": "Dispute Filing"},
            {"step": "1", "action": "Aggrieved party clicks 'Raise Dispute'", "flow": "<-", "info": "Dispute Initiation"},
            {"step": "2", "action": "System immediately halts auto-approval countdown and locks milestone escrow funds", "flow": "->", "info": "Escrow Freeze Lock"},
            {"step": "3", "action": "User selects dispute reason (Non-performance, Specification deviation, Abandonment, Unreasonable revisions)", "flow": "<-", "info": "Dispute Category"},
            {"step": "4", "action": "User uploads supporting evidence (chat logs, SOW clauses, diff files)", "flow": "<-", "info": "Evidence dossier"},
            {"step": "5", "action": "System notifies counter-party and provides 48 hours to submit rebuttal evidence", "flow": "->", "info": "Rebuttal Window Notice"},
            {"step": "6", "action": "System assigns dispute case ID and routes dossier to Escrow Mediator queue (triggers UC-21)", "flow": "->", "info": "Mediator Case Assignment"}
        ],
        "alternatives": [
            {
                "id": "16.1",
                "title": "Parties reach mutual amicable settlement before mediator verdict",
                "steps": [
                    {"step": "1", "action": "Parties negotiate direct compromise (e.g. 50/50 split of milestone)", "flow": "<-", "info": "Mutual Settlement Agreement"},
                    {"step": "2a", "action": "Both parties sign agreement digitally in dispute portal", "flow": "<-", "info": "Digital Signatures"},
                    {"step": "3a", "action": "System executes agreed split, unfreezes escrow, and closes dispute case", "flow": "->", "info": "Mutual Settlement Payout"}
                ]
            }
        ],
        "postconditions": [
            "1. Escrow funds secured against automatic liquidation.",
            "2. Formal legal dispute case established with immutable evidence timestamps."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Counter-party fails to submit rebuttal within 48 hours",
                "steps": [
                    "1. Rebuttal timer expires.",
                    "2. Case forwarded to mediator with default adverse inference note against non-responding party."
                ]
            }
        ],
        "inputs": [
            ("Dispute grounds & evidence files", "Initiating Party"),
            ("Contract SOW terms & Milestone history", "Platform Database")
        ],
        "outputs": [
            ("Escrow Freeze Command", "Escrow Ledger"),
            ("Dispute Case Dossier", "Mediator Portal"),
            ("Legal Notification", "Both Contract Parties")
        ],
        "fr_correlation": ["FR-016 (Escrow Dispute Mediation)", "FR-021 (Mediator Adjudication)"],
        "testing_mapping": {
            "positive_tests": ["TC-16-01: Verify dispute trigger instantly pauses the 72-hour auto-approval clock."],
            "boundary_tests": ["TC-16-02: Test simultaneous dispute filing from both parties for the same milestone."],
            "exception_tests": ["TC-16-03: Verify locked escrow cannot be withdrawn by either party while dispute is OPEN."]
        }
    },
    {
        "id": "UC-17",
        "name": "Calculate Creator Authority Score (CAS)",
        "priority": "High",
        "actor": "Automated System Daemon",
        "description": "The background intelligence daemon continuously computes the multi-factor Creator Authority Score (CAS) for each specialist. CAS combines credential verification level, peer attestations, completed escrow track record, client reviews, and content dwell telemetry to determine organic reach and badge tiers.",
        "trigger": "Temporal trigger: Runs hourly batch cycle, and immediately upon major events (milestone completed, credential verified).",
        "type_external": False,
        "type_temporal": True,
        "preconditions": [
            "1. Creator has published profile or active content.",
            "2. Telemetry and verification datastores are online."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Compute multi-factor Creator Authority Score", "flow": "", "info": "CAS Computation"},
            {"step": "1", "action": "System daemon gathers creator input vectors: [Registry Verification Tier (40%), Completed Escrow Contracts (30%), Case Study Saves & Dwell (20%), Peer Attestations (10%)]", "flow": "<-", "info": "Creator Vector Telemetry"},
            {"step": "2", "action": "System applies anti-gaming heuristic (detects circular reviews, self-booking, bot dwell)", "flow": "<-", "info": "Anomaly Detection Weights"},
            {"step": "3", "action": "System calculates normalized CAS score on a scale of 0 to 1,000 points", "flow": "->", "info": "Computed CAS Float"},
            {"step": "4", "action": "System updates Creator Authority Tier: [Tier 1: Emerging Creator (0-399) | Tier 2: Established Practitioner (400-699) | Tier 3: Industry Authority (700-1,000)]", "flow": "->", "info": "Updated Tier Classification"},
            {"step": "5", "action": "System writes updated CAS weights into Redis cache for high-speed feed ranking (UC-18)", "flow": "->", "info": "Redis CAS Cache Record"}
        ],
        "alternatives": [
            {
                "id": "17.1",
                "title": "Anomaly detected (Sybil attack or artificial metric inflation)",
                "steps": [
                    {"step": "1", "action": "Anti-gaming engine detects suspicious clustered IP views or circular payments", "flow": "<-", "info": "Fraud Anomaly Flag"},
                    {"step": "2a", "action": "System dampens score gain and flags profile for Trust & Safety review (UC-20)", "flow": "->", "info": "Trust & Safety Alert"}
                ]
            }
        ],
        "postconditions": [
            "1. Creator CAS updated across all platform services.",
            "2. Feed recommendation weights adjusted."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Missing telemetry partitions during calculation",
                "steps": [
                    "1. Daemon utilizes last known valid CAS score.",
                    "2. Error logged to system monitoring; calculation rescheduled in 15 minutes."
                ]
            }
        ],
        "inputs": [
            ("Registry data, completed milestone records, dwell telemetry", "Platform Datastores")
        ],
        "outputs": [
            ("Updated CAS Score & Authority Tier", "Creator Profile & Redis Cache"),
            ("Feed Ranking Multiplier", "Discovery Recommendation Pipeline")
        ],
        "fr_correlation": ["FR-017 (Creator Authority Scoring Engine)", "FR-018 (Algorithmic Ranking)"],
        "testing_mapping": {
            "positive_tests": ["TC-17-01: Verify adding verified LSK license increases CAS by precisely calculated 40% weight."],
            "boundary_tests": ["TC-17-02: Test CAS calculation across 100,000 active creators within 60-second batch window."],
            "exception_tests": ["TC-17-03: Verify circular booking ring is flagged and receives zero CAS boost."]
        }
    },
    {
        "id": "UC-18",
        "name": "Personalize Two-Pass Discovery Feed",
        "priority": "High",
        "actor": "Automated System Daemon",
        "description": "The AI recommendation engine executes a two-pass algorithm to serve ultra-relevant, authoritative content to every user. Pass 1 conducts high-speed candidate retrieval via vector embeddings; Pass 2 performs heavy business re-ranking incorporating CAS scores, geographic relevance (Kenya/East Africa), and personal interest.",
        "trigger": "External request from UC-01 (client loading feed) or client session update.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Vector embedding store (pgvector/Pinecone) is indexed.",
            "2. Pre-computed CAS weights available in Redis."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Execute two-pass candidate retrieval and ranking", "flow": "", "info": "Feed Personalization"},
            {"step": "1", "action": "Recommendation worker receives client request with session context and location", "flow": "<-", "info": "Client Context Vector"},
            {"step": "2", "action": "Pass 1 (Candidate Retrieval): System retrieves top 200 candidates via Approximate Nearest Neighbor (ANN) vector search", "flow": "<-", "info": "200 Candidate Case Studies"},
            {"step": "3", "action": "Pass 2 (Business Re-Ranking): System scores each candidate: Score = (Cosine Similarity * 0.35) + (CAS * 0.40) + (GeoRelevance * 0.15) + (Freshness * 0.10)", "flow": "->", "info": "Weighted Rank Matrix"},
            {"step": "4", "action": "System applies diversity filter to ensure no single creator dominates more than 2 consecutive cards", "flow": "->", "info": "Deduplicated Stream"},
            {"step": "5", "action": "System returns top 20 ranked case studies to client feed loader", "flow": "->", "info": "Top 20 Ranked Cards"}
        ],
        "alternatives": [
            {
                "id": "18.1",
                "title": "Cold start: New guest user with zero prior browsing history",
                "steps": [
                    {"step": "1", "action": "System detects unauthenticated guest or zero-history profile", "flow": "<-", "info": "Cold Start Flag"},
                    {"step": "2a", "action": "Pass 1 retrieves platform-wide top trending case studies from Tier 3 Industry Authorities", "flow": "<-", "info": "Trending Authority Candidates"},
                    {"step": "3a", "action": "Pass 2 optimizes for broad cross-disciplinary diversity (Tech, Legal, Finance)", "flow": "->", "info": "Curated Onboarding Stream"}
                ]
            }
        ],
        "postconditions": [
            "1. Feed payload delivered to client app in under 200ms.",
            "2. Ranking weights logged for ML model performance evaluation."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Vector store response latency exceeds 150ms timeout",
                "steps": [
                    "1. Circuit breaker trips immediately.",
                    "2. System serves pre-ranked fallback cache from Redis in <20ms."
                ]
            }
        ],
        "inputs": [
            ("Client session vector & location", "Client App Request"),
            ("Case study embeddings & CAS weights", "Vector Store & Redis Cache")
        ],
        "outputs": [
            ("Ranked Feed Payload (Top 20 items)", "Client App"),
            ("Ranking Telemetry Logs", "ML Pipeline")
        ],
        "fr_correlation": ["FR-018 (Two-Pass Recommendation Architecture)", "FR-001 (Feed Delivery)"],
        "testing_mapping": {
            "positive_tests": ["TC-18-01: Verify Pass 2 re-ranking boosts Tier 3 author content ahead of higher cosine match with Tier 1 author."],
            "boundary_tests": ["TC-18-02: Test feed diversity filter guarantees no single author has >2 cards in top 10."],
            "exception_tests": ["TC-18-03: Verify circuit breaker fallback delivers cached feed in < 30ms during vector DB crash."]
        }
    },
    {
        "id": "UC-19",
        "name": "Manage Phased Rollout & Creator Onboarding",
        "priority": "Medium",
        "actor": "Platform Administrator",
        "description": "The Administrator manages the controlled phased rollout of Consult Kenya. The workflow governs transitions across Phase 1 (Anchor Agency Onboarding), Phase 2 (Curated Beta with invite codes), and Phase 3 (Open Ecosystem with automated verification).",
        "trigger": "Admin updates rollout parameters in Admin Console.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Admin is authenticated with superuser MFA permissions."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Configure platform rollout phase and creator quotas", "flow": "", "info": "Rollout Governance"},
            {"step": "1", "action": "Admin accesses Rollout Governance dashboard", "flow": "<-", "info": "Admin Access"},
            {"step": "2", "action": "Admin views current cohort statistics: [Active Creators, Pending Invites, Verification Backlog, Take Rate]", "flow": "->", "info": "Cohort Metrics"},
            {"step": "3", "action": "Admin generates batch of 50 VIP Invite Codes for curated pilot consultants", "flow": "<-", "info": "Invite Code Generation Command"},
            {"step": "4", "action": "System produces cryptographically signed, one-time invite tokens", "flow": "->", "info": "Invite Tokens"},
            {"step": "5", "action": "Admin configures platform take rate (e.g., set to introductory 5% for Phase 1 partners)", "flow": "<-", "info": "Take rate configuration"},
            {"step": "6", "action": "System updates billing engine parameters across all new contract initializations", "flow": "->", "info": "Updated Billing Config"}
        ],
        "alternatives": [
            {
                "id": "19.1",
                "title": "Admin triggers rollout transition to Phase 3 (Open Ecosystem)",
                "steps": [
                    {"step": "1", "action": "Admin selects 'Activate Open Ecosystem'", "flow": "<-", "info": "Open Phase Command"},
                    {"step": "2a", "action": "System removes invite code requirement and enables automated registry self-onboarding", "flow": "->", "info": "Public Onboarding Enabled"}
                ]
            }
        ],
        "postconditions": [
            "1. Updated rollout policy enforced platform-wide.",
            "2. Admin action logged in security audit vault."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Unauthorized attempt to modify platform take rate without secondary approval",
                "steps": [
                    "1. System requires second admin multi-signature sign-off for financial parameter changes.",
                    "2. Change remains pending until second admin approves."
                ]
            }
        ],
        "inputs": [
            ("Rollout phase toggle, invite batches, commission rates", "Platform Administrator")
        ],
        "outputs": [
            ("Cryptographic Invite Codes", "Admin Dashboard"),
            ("Updated Platform Operational Parameters", "System Configuration DB")
        ],
        "fr_correlation": ["FR-019 (Phased Rollout Management)", "FR-020 (Admin Governance)"],
        "testing_mapping": {
            "positive_tests": ["TC-19-01: Verify valid invite code grants creator onboarding access during Phase 2 Curated Beta."],
            "boundary_tests": ["TC-19-02: Test invite code exhaustion after single use."],
            "exception_tests": ["TC-19-03: Verify take rate modification requires dual admin approval."]
        }
    },
    {
        "id": "UC-20",
        "name": "Moderate Platform Content & Enforce NDAs",
        "priority": "High",
        "actor": "Platform Administrator / Compliance Officer",
        "description": "The Administrator and automated moderation daemons review flagged case studies, prevent enterprise non-disclosure agreement (NDA) leaks, detect spam, and redact unauthorized proprietary client information.",
        "trigger": "External: User flags a case study; Automated: Content ingestion scanner detects potential client confidential data.",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Case study submitted or reported.",
            "2. Automated DLP (Data Loss Prevention) regex scanners active."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Audit flagged content and enforce compliance action", "flow": "", "info": "Content Moderation"},
            {"step": "1", "action": "System flags case study containing high-risk tokens (e.g. unredacted bank account numbers, API secrets, confidential client names)", "flow": "<-", "info": "DLP Scanner Trigger"},
            {"step": "2", "action": "System moves case study to 'PENDING_MODERATION' and notifies reviewer", "flow": "->", "info": "Moderation Queue Item"},
            {"step": "3", "action": "Compliance Officer inspects highlighted sensitive text snippets in split-screen diff tool", "flow": "<-", "info": "Audit View"},
            {"step": "4", "action": "Officer applies automated Redactor tool to blur sensitive figures while preserving educational architecture", "flow": "<-", "info": "Redaction Command"},
            {"step": "5", "action": "Officer approves sanitized version and publishes deck", "flow": "->", "info": "Sanitized Case Study"},
            {"step": "6", "action": "System sends compliance advisory note to author", "flow": "->", "info": "Author Compliance Note"}
        ],
        "alternatives": [
            {
                "id": "20.1",
                "title": "Severe violation (plagiarism, willful breach of corporate trade secret, malicious code)",
                "steps": [
                    {"step": "1", "action": "Officer selects 'Take Down & Issue Strike'", "flow": "<-", "info": "Take-down Command"},
                    {"step": "2a", "action": "System removes deck from public feed immediately, adds strike to author profile, and docks CAS points by 200", "flow": "->", "info": "Enforcement Action"}
                ]
            }
        ],
        "postconditions": [
            "1. Platform remains free from trade secret liability.",
            "2. Comprehensive audit trail recorded."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "Author files dispute against moderation take-down",
                "steps": [
                    "1. Author submits proof of authorization or written client consent.",
                    "2. Senior legal counsel reviews and can reinstate post."
                ]
            }
        ],
        "inputs": [
            ("Flagged content, reports, scanner detections", "System / Users"),
            ("Moderation decisions & redactions", "Compliance Officer")
        ],
        "outputs": [
            ("Sanitized Published Content / Takedown Notice", "Public Platform"),
            ("Author Infraction Record", "Creator Profile Ledger")
        ],
        "fr_correlation": ["FR-020 (Content Moderation & NDA Redaction)", "FR-017 (CAS Penalties)"],
        "testing_mapping": {
            "positive_tests": ["TC-20-01: Verify DLP scanner flags AWS API keys or KRA PINs in code blocks before publish."],
            "boundary_tests": ["TC-20-02: Test automated take-down latency (< 1 second) upon critical trade secret notice."],
            "exception_tests": ["TC-20-03: Verify docked CAS points properly recalculate creator's rank."]
        }
    },
    {
        "id": "UC-21",
        "name": "Adjudicate Milestone Dispute",
        "priority": "Medium",
        "actor": "Escrow Mediator / Legal Counsel",
        "description": "An appointed Escrow Mediator evaluates evidence submitted by both Client and Consultant in a disputed milestone, interprets contractual SOW acceptance criteria, and issues a legally binding apportionment and fund disbursement ruling.",
        "trigger": "Mediator opens pending case from Escrow Dispute Queue (following UC-16).",
        "type_external": True,
        "type_temporal": False,
        "preconditions": [
            "1. Dispute case opened with both claimant dossier and respondent rebuttal.",
            "2. Milestone funds frozen in escrow vault."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Adjudicate milestone dispute and disburse escrow", "flow": "", "info": "Dispute Adjudication"},
            {"step": "1", "action": "Mediator reviews SOW deliverables, GitHub commits, milestone artifacts, and chat transcripts", "flow": "<-", "info": "Case Evidence Dossier"},
            {"step": "2", "action": "Mediator conducts independent technical or domain verification (e.g. audits if code compiles or tax memo meets standards)", "flow": "<-", "info": "Independent audit findings"},
            {"step": "3", "action": "Mediator enters adjudication decision: [Full Release to Consultant | Full Refund to Client | Prorated Settlement (e.g. 60% Consultant, 40% Client)]", "flow": "<-", "info": "Adjudication Verdict"},
            {"step": "4", "action": "Mediator inputs written justification rationale citing contract clause numbers", "flow": "<-", "info": "Legal Ruling Rationale"},
            {"step": "5", "action": "System prompts Mediator for biometric / hardware token approval", "flow": "<-", "info": "Mediator Security Token"},
            {"step": "6", "action": "System executes binding fund disbursement from escrow according to verdict", "flow": "->", "info": "Disbursement Execution"},
            {"step": "7", "action": "System issues formal Adjudication Certificate PDF to both parties and closes dispute case", "flow": "->", "info": "Adjudication Certificate PDF"}
        ],
        "alternatives": [
            {
                "id": "21.1",
                "title": "Mediator requests additional clarifying documentation from parties",
                "steps": [
                    {"step": "1", "action": "Mediator issues formal request for supplemental evidence with 24-hour deadline", "flow": "->", "info": "Request for Evidence"},
                    {"step": "2a", "action": "Parties upload requested files; mediator resumes review at step 2", "flow": "<-", "info": "Supplemental files"}
                ]
            }
        ],
        "postconditions": [
            "1. Frozen escrow funds liquidated and disbursed to determined parties.",
            "2. Dispute marked 'CLOSED_RESOLVED'.",
            "3. Permanent record logged in legal archive."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "System detects potential conflict of interest between mediator and participant",
                "steps": [
                    "1. Algorithm flags shared prior engagements.",
                    "2. Case automatically reassigned to alternate neutral mediator."
                ]
            }
        ],
        "inputs": [
            ("Dispute case evidence, SOW, Deliverables", "Dispute Vault"),
            ("Mediator verdict & legal rationale", "Escrow Mediator")
        ],
        "outputs": [
            ("Escrow Disbursement Commands", "Platform Payment Rails"),
            ("Adjudication Certificate PDF", "Client & Consultant"),
            ("Immutable Legal Audit Log", "Platform Regulatory Vault")
        ],
        "fr_correlation": ["FR-021 (Escrow Dispute Adjudication)", "FR-016 (Dispute Intake)"],
        "testing_mapping": {
            "positive_tests": ["TC-21-01: Verify prorated ruling (e.g., 70/30) executes exact currency math without fractional cent loss."],
            "boundary_tests": ["TC-21-02: Test mediator ruling on zero-balance or expired authorization."],
            "exception_tests": ["TC-21-03: Verify mediator verdict cannot be altered once digitally signed."]
        }
    },
    {
        "id": "UC-22",
        "name": "Audit Financial Settlement & Tax Compliance",
        "priority": "High",
        "actor": "Escrow Mediator / Platform Financial Auditor",
        "description": "The Financial Auditor reviews platform ledger transactions, verifies withholding tax calculations, audits statutory KRA eTIMS submissions, and ensures full compliance with Kenyan data and financial regulations.",
        "trigger": "Temporal trigger: End-of-month financial closing; External trigger: Audit inspection.",
        "type_external": False,
        "type_temporal": True,
        "preconditions": [
            "1. Financial period closed or audit scope selected.",
            "2. Double-entry ledger is reconciled."
        ],
        "normal_course": [
            {"step": "1.0", "action": "Perform statutory financial settlement and tax audit", "flow": "", "info": "Financial Audit"},
            {"step": "1", "action": "Auditor selects reporting period (e.g., September 2026 Monthly Settlement)", "flow": "<-", "info": "Audit Period Parameters"},
            {"step": "2", "action": "System aggregates all transactions: [Total Bookings, Escrow Disbursements, Platform Take Rates, KRA Withholding Taxes]", "flow": "->", "info": "Reconciled Ledger Balance Sheet"},
            {"step": "3", "action": "System queries KRA eTIMS API to verify that all electronic tax receipts match ledger records", "flow": "<-", "info": "KRA eTIMS API Reconciliation Status"},
            {"step": "4", "action": "System runs checksum verification between M-Pesa B2C statements, bank RTGS accounts, and internal ledger", "flow": "->", "info": "Three-Way Reconciliation Matrix"},
            {"step": "5", "action": "Auditor inspects any variances or flagged reconciliations", "flow": "<-", "info": "Auditor Sign-off"},
            {"step": "6", "action": "System exports statutory monthly tax compliance report and seals period with cryptographic hash", "flow": "->", "info": "Sealed Financial Audit Report"}
        ],
        "alternatives": [
            {
                "id": "22.1",
                "title": "Discrepancy detected during three-way reconciliation (e.g. unapplied bank charge)",
                "steps": [
                    {"step": "1", "action": "System flags variance (> KES 0.00) between bank statement and ledger", "flow": "->", "info": "Discrepancy Alert"},
                    {"step": "2a", "action": "Auditor traces transaction UUID to specific failed webhook or bank service fee", "flow": "<-", "info": "Trace Query"},
                    {"step": "3a", "action": "Auditor creates adjusting journal entry with documented reason", "flow": "<-", "info": "Adjusting Journal Entry"},
                    {"step": "4a", "action": "Ledger balance reconciles to zero variance", "flow": "->", "info": "Zero Variance Status"}
                ]
            }
        ],
        "postconditions": [
            "1. Monthly financial ledger closed and sealed against further modification.",
            "2. Statutory eTIMS tax filings certified and archived for 7-year regulatory retention."
        ],
        "exceptions": [
            {
                "id": "E1",
                "title": "KRA eTIMS API gateway down during end-of-month batch synchronization",
                "steps": [
                    "1. System buffers unconfirmed tax invoices in offline resilient compliance queue.",
                    "2. Automatic exponential backoff retries submission once KRA services restore.",
                    "3. Auditor notified with automated status tracker."
                ]
            }
        ],
        "inputs": [
            ("Audit parameters & adjustments", "Financial Auditor"),
            ("KRA eTIMS validation records & Bank statements", "External Financial Rails")
        ],
        "outputs": [
            ("Three-Way Reconciliation Statement", "Auditor Screen"),
            ("Cryptographically Sealed Tax Audit Package", "Kenya Revenue Authority & Internal Archive")
        ],
        "fr_correlation": ["FR-022 (Tax & eTIMS Compliance)", "FR-013 (Escrow Ledger)"],
        "testing_mapping": {
            "positive_tests": ["TC-22-01: Verify three-way reconciliation confirms zero mathematical discrepancy across 10,000 transactions."],
            "boundary_tests": ["TC-22-02: Test ledger audit sealing prevents subsequent retroactive row modification (tamper-proofing)."],
            "exception_tests": ["TC-22-03: Verify resilient tax queue preserves exact invoice timestamps during 48-hour KRA outage."]
        }
    }
]

# Generate individual markdown files
for uc in use_cases_data:
    filename = f"{uc['id']}_{uc['name'].replace(' ', '_').replace('&', 'And').replace('/', '_').replace('-', '_').replace('(', '').replace(')', '')}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Build markdown table matching the user's reference diagram
    ext_check = "[x] External" if uc["type_external"] else "[ ] External"
    temp_check = "[x] Temporal" if uc["type_temporal"] else "[ ] Temporal"
    
    md = []
    md.append(f"# Use Case Specification: {uc['name']}")
    md.append(f"**Use Case Name:** {uc['name']} | **ID:** `{uc['id']}` | **Priority:** {uc['priority']}\n")
    md.append(f"**Actor:** {uc['actor']}")
    md.append(f"**Description:** {uc['description']}")
    md.append(f"**Trigger:** {uc['trigger']}")
    md.append(f"**Type:** {ext_check}  {temp_check}\n")
    
    md.append("### Preconditions")
    for pre in uc["preconditions"]:
        md.append(f"{pre}")
    md.append("")
    
    md.append("---")
    md.append("### Execution Steps & Information Flow")
    md.append("*(Follows Dennis, Wixom & Tegarden SAD Standard with directional data flow arrows)*\n")
    
    md.append("#### Normal Course")
    md.append("| Step | Action / Activity Performed | Flow | Information for Step |")
    md.append("| :--- | :--- | :---: | :--- |")
    for step in uc["normal_course"]:
        flow_arrow = ""
        if step["flow"] == "<-":
            flow_arrow = "$\longleftarrow$"
        elif step["flow"] == "->":
            flow_arrow = "$\longrightarrow$"
        md.append(f"| **{step['step']}** | {step['action']} | {flow_arrow} | {step['info']} |")
    md.append("")
    
    if uc["alternatives"]:
        md.append("#### Alternative Courses")
        for alt in uc["alternatives"]:
            md.append(f"**{alt['id']} {alt['title']}**\n")
            md.append("| Step | Action / Activity Performed | Flow | Information for Step |")
            md.append("| :--- | :--- | :---: | :--- |")
            for step in alt["steps"]:
                flow_arrow = ""
                if step["flow"] == "<-":
                    flow_arrow = "$\longleftarrow$"
                elif step["flow"] == "->":
                    flow_arrow = "$\longrightarrow$"
                md.append(f"| {step['step']} | {step['action']} | {flow_arrow} | {step['info']} |")
            md.append("")
            
    md.append("### Postconditions")
    for post in uc["postconditions"]:
        md.append(f"{post}")
    md.append("")
    
    md.append("### Exceptions")
    for exc in uc["exceptions"]:
        md.append(f"**{exc['id']}: {exc['title']}**")
        for s in exc["steps"]:
            md.append(f"{s}")
        md.append("")
        
    md.append("---")
    md.append("### Summary Inputs & Outputs")
    md.append("| Summary Inputs | Source | Outputs | Destination |")
    md.append("| :--- | :--- | :--- | :--- |")
    
    max_len = max(len(uc["inputs"]), len(uc["outputs"]))
    for i in range(max_len):
        inp_str = uc["inputs"][i][0] if i < len(uc["inputs"]) else ""
        src_str = uc["inputs"][i][1] if i < len(uc["inputs"]) else ""
        out_str = uc["outputs"][i][0] if i < len(uc["outputs"]) else ""
        dst_str = uc["outputs"][i][1] if i < len(uc["outputs"]) else ""
        md.append(f"| {inp_str} | {src_str} | {out_str} | {dst_str} |")
    md.append("")
    
    md.append("---")
    md.append("### Systems Analysis Traceability & Verification")
    md.append(f"**Correlated Functional Requirements:** {', '.join(uc['fr_correlation'])}\n")
    md.append("**Testing Strategy & Acceptance Test Cases:**")
    md.append("- **Positive Test Cases (Normal Course):**")
    for pt in uc["testing_mapping"]["positive_tests"]:
        md.append(f"  - `{pt}`")
    md.append("- **Boundary & Alternative Test Cases:**")
    for bt in uc["testing_mapping"]["boundary_tests"]:
        md.append(f"  - `{bt}`")
    md.append("- **Negative & Exception Test Cases:**")
    for et in uc["testing_mapping"]["exception_tests"]:
        md.append(f"  - `{et}`")
    md.append("")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

print(f"Generated {len(use_cases_data)} detailed use case specifications in {output_dir}")
