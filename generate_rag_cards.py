import json
import os
import math
import re

# Complete set of structured RAG cards extracted from KenyaConsult.pdf
cards = [
    {
        "card_id": "CARD-001",
        "category": "Brand & Identity",
        "topic": "Platform Identity & Naming Strategy",
        "source_file": "KenyaConsult.pdf",
        "page_number": 1,
        "summary": "Selection of 'Consult Kenya' over 'Kenyan Consult' to establish an expansive national ecosystem rather than a closed private boutique firm.",
        "key_entities": ["Consult Kenya", "Kenyan Consult", "Brand Identity"],
        "content": (
            "User explores building an ecosystem combining Instagram's visual feed and swipeable simplicity with LinkedIn's "
            "professional consulting authority. Between 'Consult Kenya' and 'Kenyan Consult', Consult Kenya is selected. "
            "'Kenyan Consult' sounds like a closed private firm, whereas 'Consult Kenya' represents an overarching national "
            "ecosystem, digital advisory hub, and curated marketplace for top-tier Kenyan and African professionals."
        ),
        "grounded_rules": [
            "Brand name is definitively 'Consult Kenya'.",
            "Operates as an overarching national ecosystem, not a closed single agency."
        ],
        "tags": ["#Branding", "#PlatformIdentity", "#Ecosystem"]
    },
    {
        "card_id": "CARD-002",
        "category": "Business Model",
        "topic": "3-Phase Evolution Roadmap (Agency-First Flywheel)",
        "source_file": "KenyaConsult.pdf",
        "page_number": 2,
        "summary": "Solves marketplace cold-start via an agency-first flywheel transitioning across three distinct phases: Anchor Agency, Curated Cohort, and Open Ecosystem.",
        "key_entities": ["Anchor Agency", "Curated Cohort", "Open Ecosystem", "Marketplace Flywheel"],
        "content": (
            "Phased Rollout:\n"
            "- Phase 1 (Anchor Agency): Proprietary consulting and systems architecture agency. Uses the platform mechanics exclusively to publish its own work (system architectures, legal frameworks, case studies), proving concept and pulling high-value inbound clients.\n"
            "- Phase 2 (Curated Cohort): Invite-only beta of trusted peer creators (specialized developers, corporate lawyers, brand strategists) acting as founding creators to populate the feed and calibrate multi-creator algorithms.\n"
            "- Phase 3 (Open Ecosystem): Full self-service onboarding for vetted professionals across Kenya and East Africa with multi-tenant architecture, verified credentials, and direct booking."
        ),
        "grounded_rules": [
            "Phase 1 drives 100% of initial content via proprietary agency.",
            "Phase 2 admits only vetted founding creators by invitation.",
            "Phase 3 unlocks open vetted onboarding and multi-tenancy."
        ],
        "tags": ["#Roadmap", "#BusinessModel", "#ColdStart", "#Marketplace"]
    },
    {
        "card_id": "CARD-003",
        "category": "Architecture & Principles",
        "topic": "Core Architectural Pillars",
        "source_file": "KenyaConsult.pdf",
        "page_number": 3,
        "summary": "Four foundational structural pillars: Scannable Case Study, Authority-First Discovery, Living Portfolio, and Frictionless Conversion.",
        "key_entities": ["Scannable Case Study", "Authority-First Discovery", "Living Portfolio", "Frictionless Conversion"],
        "content": (
            "Foundational axiom: Visual Proof of Professional Authority.\n"
            "1. Scannable Case Study: Replaces dense articles/static resumes with swipeable, high-contrast visual decks/carousels (e.g. 5-step compliance checklist or system architecture migration map).\n"
            "2. Authority-First Discovery: Ranks content on professional utility (bookmarks, peer shares, technical depth among verified specialists) rather than viral fluff.\n"
            "3. Living Portfolio: Profiles are modular galleries where each post acts as a verified block of real work history.\n"
            "4. Frictionless Conversion (Scroll to Contract): Direct, low-friction action trigger on every post (book consultation, technical audit, framework download)."
        ),
        "grounded_rules": [
            "Every post must contain visual proof of professional authority.",
            "Every post must attach a frictionless conversion trigger."
        ],
        "tags": ["#Pillars", "#Architecture", "#Authority", "#Conversion"]
    },
    {
        "card_id": "CARD-004",
        "category": "UI/UX & Interaction",
        "topic": "Dual-Mode Engagement UX Model",
        "source_file": "KenyaConsult.pdf",
        "page_number": 3,
        "summary": "Separation of user engagement into two contextual modes: Grid/Card Layout for inspection/due diligence, and Vertical Stream for discovery/inspiration.",
        "key_entities": ["Dual-Mode Engagement", "Grid Layout", "Vertical Stream", "Discovery vs Due Diligence"],
        "content": (
            "Separates browsing into two distinct mindsets without clashing:\n"
            "1. Grid / Bento-Box Card Layout ('Portfolio & Inspection Mode'): Used on user profiles, search results, topic hubs, and bookmarks. Delivers a high-density bird's-eye view allowing clients to scan authority baseline in 5 seconds.\n"
            "2. Vertical Stream ('Serendipity & Discovery Mode'): Used on the main Home feed. Immersive, full-screen vertical feed delivering bite-sized 30-second system breakdowns or visual carousels.\n"
            "Bridge: User spots a breakdown in vertical feed, taps profile, and instantly lands in the structured grid portfolio."
        ),
        "grounded_rules": [
            "Vertical stream is reserved for Home feed discovery.",
            "Grid/Bento layout is reserved for Profiles, Topic Hubs, and Search inspection.",
            "Both modes exist in the app but are separated contextually by user intent."
        ],
        "tags": ["#UIUX", "#DualMode", "#BentoGrid", "#VerticalStream"]
    },
    {
        "card_id": "CARD-005",
        "category": "UI/UX & Navigation",
        "topic": "5-Tab Structural Navigation & Contextual Toggles",
        "source_file": "KenyaConsult.pdf",
        "page_number": 4,
        "summary": "Primary 5-tab Bottom Navigation hierarchy paired with contextual micro-view toggles on specific sub-pages.",
        "key_entities": ["Bottom Navigation Bar", "5-Tab Structure", "Contextual Toggle"],
        "content": (
            "Primary Navigation Hierarchy:\n"
            "1. Home: Vertical Stream for passive discovery and video/carousel feeds.\n"
            "2. Explore / Hubs: Multi-column Bento Grid for active topic searches (#SoftwareArchitecture, #CorporateLaw, #TaxStrategy).\n"
            "3. Publish / Create: Center action button launching the Creation Studio.\n"
            "4. Activity / Messages: Chat, notifications, direct inquiries, and booking confirmations.\n"
            "5. Profile: Dedicated Bento-box portfolio grid representing the permanent execution record.\n"
            "Contextual Toggles: Used locally inside profiles/search (e.g. Visual Grid vs Chronological Feed toggle) rather than global top-level switches."
        ),
        "grounded_rules": [
            "Global navigation uses a 5-tab Bottom Bar.",
            "Contextual sub-toggles (Grid vs Chronological) are strictly scoped inside Profile and Search views."
        ],
        "tags": ["#Navigation", "#BottomNav", "#InformationArchitecture"]
    },
    {
        "card_id": "CARD-006",
        "category": "Publishing & Workflow",
        "topic": "4-Step Creation Studio Flow",
        "source_file": "KenyaConsult.pdf",
        "page_number": 5,
        "summary": "Optimized publishing flow designed to eliminate blank-page syndrome while enforcing enterprise-grade structural depth.",
        "key_entities": ["Creation Studio", "Template Engine", "Evidence Layer", "Conversion Anchor"],
        "content": (
            "4-Step Studio Pipeline:\n"
            "Step 1 - Format Selection: Swipeable Carousel (step-by-step guides, code/architecture maps), Vertical Micro-Video (30-60s walkthrough), or Blueprint Card (single schema/UI showcase).\n"
            "Step 2 - Structured Template Engine: Fill-in-the-blank narrative frameworks:\n"
            "  * Template A (Case Study): Challenge -> Architecture/Solution -> Business Impact\n"
            "  * Template B (Explainer): Core Concept -> Common Pitfalls -> Best Practice Framework\n"
            "  * Template C (Toolkit): Problem -> Recommended Tools/Stack -> Actionable Template\n"
            "  * Auto-Styling applies clean typography, code syntax blocks, and brand cards.\n"
            "Step 3 - Evidence & Credential Tagging: Attach verifiable proof (GitHub repo, live URL, case document, skill tags, co-author/client tags).\n"
            "Step 4 - Conversion Anchor: Attach direct business call-to-action (Book 15-min call, Request technical audit, Download framework PDF, Inquire retainer)."
        ),
        "grounded_rules": [
            "Posts must follow a structured narrative template.",
            "Auto-styling handles high-contrast typography and syntax formatting.",
            "Every published post must have at least one conversion anchor and evidence link."
        ],
        "tags": ["#CreationStudio", "#PublishingFlow", "#Templates", "#CallToAction"]
    },
    {
        "card_id": "CARD-007",
        "category": "Algorithms & Ranking",
        "topic": "Multi-Objective Authority Engine & Scoring Model",
        "source_file": "KenyaConsult.pdf",
        "page_number": 7,
        "summary": "Algorithmic discovery engine replacing viral clickbait with verified professional substance, authority scoring, and multi-objective ranking.",
        "key_entities": ["Creator Authority Score", "Multi-Objective Ranking", "Bookmark Weight", "Dwell Time"],
        "content": (
            "Algorithmic Architecture:\n"
            "1. Authority-Weighted Scoring Model: Modulates raw interaction velocity with Creator Authority Score based on verified credentials, completed projects, and enterprise history.\n"
            "2. Multi-Objective Ranking Metrics:\n"
            "   * Dwell Time & Completion Rate: Tracks carousel slide dwell time and video completion.\n"
            "   * Bookmark / Save Rate: Core professional indicator carrying 5x the algorithmic weight of a standard like.\n"
            "   * Conversion Intent: Measures click-throughs to portfolio links, booking modals, or framework downloads."
        ),
        "grounded_rules": [
            "Raw engagement is multiplied by Creator Authority Score.",
            "Save/Bookmark actions carry 5x weight compared to likes.",
            "High dwell time boosts distribution."
        ],
        "tags": ["#Algorithm", "#AuthorityScoring", "#MultiObjectiveRanking", "#Feed"]
    },
    {
        "card_id": "CARD-008",
        "category": "Algorithms & Search",
        "topic": "Two-Pass AI Retrieval Engine",
        "source_file": "KenyaConsult.pdf",
        "page_number": 8,
        "summary": "Two-pass semantic candidate generation and heavy business ranking for discovery feed personalization.",
        "key_entities": ["Candidate Retrieval", "Heavy Ranking", "Semantic Embeddings", "Local Context"],
        "content": (
            "Two-Pass Feed Recommendation Architecture:\n"
            "- Pass 1 (Candidate Retrieval): LLM-based embeddings match viewer profile history (skills, active projects, past bookmarks) with content tags (#TaxLaw, #React, #SupplyChain) to retrieve candidate pools even under cold-start conditions.\n"
            "- Pass 2 (Heavy Ranking): Applies business logic scoring combining creator authority tier, regional relevance (prioritizing East African and Kenyan market context), and velocity to assemble the final top 20 feed items."
        ),
        "grounded_rules": [
            "Pass 1 performs vector similarity retrieval against user profile interests.",
            "Pass 2 applies regional East Africa weighting, authority tier, and velocity."
        ],
        "tags": ["#TwoPassAI", "#Embeddings", "#RecommendationSystem", "#Search"]
    },
    {
        "card_id": "CARD-009",
        "category": "Monetization & Payments",
        "topic": "Native Booking Engine & Payment Rails",
        "source_file": "KenyaConsult.pdf",
        "page_number": 8,
        "summary": "Zero-friction in-app calendar scheduling modal paired with dual local M-Pesa STK push and international card processing.",
        "key_entities": ["In-App Booking Modal", "M-Pesa STK Push", "Payment Rails", "Paystack/Flutterwave"],
        "content": (
            "Embedded Booking & Payment Flow:\n"
            "1. In-App Modal: Tapping a conversion anchor slides up a native calendar booking sheet. Pulls real-time consultant availability without external redirection.\n"
            "2. Dual-Market Payment Rails:\n"
            "   * Local Layer (Kenya/East Africa): M-Pesa STK Push via Paystack or Flutterwave for frictionless mobile checkout.\n"
            "   * International Layer: Multi-currency credit card processing (Visa, Mastercard, USD/EUR) for global and diaspora clients.\n"
            "3. Instant Confirmation: Auto-books slot, generates video meeting link, and delivers calendar invites to both parties."
        ),
        "grounded_rules": [
            "Booking is entirely native via in-app slide-up modal (no external redirects).",
            "M-Pesa STK Push is mandatory for East African users.",
            "International cards (Visa/Mastercard) are supported for cross-border bookings."
        ],
        "tags": ["#BookingEngine", "#MPesa", "#Payments", "#Checkout"]
    },
    {
        "card_id": "CARD-010",
        "category": "Commercial & Trust",
        "topic": "Milestone Escrow Protection & Revenue Model",
        "source_file": "KenyaConsult.pdf",
        "page_number": 9,
        "summary": "Enterprise milestone escrow mechanism to de-risk high-value B2B projects, coupled with phased platform monetization take rates.",
        "key_entities": ["Milestone Escrow", "Deliverable Approval", "Platform Take Rate", "SaaS Pro Profiles"],
        "content": (
            "1. Milestone Escrow Protection: For project contracts (multi-week builds, tax restructuring), funds are held in platform escrow. Consultant breaks engagement into milestones; funds release to payout wallet upon client deliverable approval.\n"
            "2. Phased Revenue Architecture:\n"
            "   * Phase 1 (Agency): 100% of revenue flows to the internal consulting agency.\n"
            "   * Phase 2 & 3 (Open Platform): 5% to 8% platform take rate on processed bookings/escrow to cover gateway, escrow, and dispute handling.\n"
            "   * SaaS Tiering (Pro Profiles): Subscription fee for advanced analytics, unbranded custom client portals, and priority search placement."
        ),
        "grounded_rules": [
            "Milestone funds are locked in escrow until explicit client sign-off.",
            "Platform charges 5% - 8% take rate during open platform phases.",
            "Pro profiles offer premium analytics and priority discovery."
        ],
        "tags": ["#Escrow", "#Monetization", "#TakeRate", "#SaaS"]
    }
]

# Ensure output directory
os.makedirs("rag_knowledge/cards", exist_ok=True)
os.makedirs("rag_knowledge/index", exist_ok=True)

# Save master cards JSON
cards_file = "rag_knowledge/cards/cards_master.json"
with open(cards_file, "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

print(f"Saved {len(cards)} RAG cards to {cards_file}")

# Write Markdown summary of cards
md_file = "rag_knowledge/cards/cards_summary.md"
with open(md_file, "w", encoding="utf-8") as f:
    f.write("# Consult Kenya - Structured RAG Knowledge Cards\n\n")
    f.write(f"Generated from `KenyaConsult.pdf` | Total Atomic Cards: {len(cards)}\n\n---\n\n")
    for c in cards:
        f.write(f"## [{c['card_id']}] {c['topic']}\n")
        f.write(f"- **Category:** `{c['category']}`\n")
        f.write(f"- **Source:** `{c['source_file']}` (Page {c['page_number']})\n")
        f.write(f"- **Summary:** {c['summary']}\n")
        f.write(f"- **Key Entities:** {', '.join(c['key_entities'])}\n")
        f.write(f"- **Grounded Rules:**\n")
        for r in c['grounded_rules']:
            f.write(f"  - {r}\n")
        f.write(f"\n```text\n{c['content']}\n```\n\n---\n\n")

print(f"Saved Markdown summary to {md_file}")
