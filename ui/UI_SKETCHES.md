# Phase 9.1: Annotated UI Sketches (Crazy Eights Synthesis)
*System: Consult Kenya (Visual-First Professional Advisory & Authority Network)*
*Grounded in RAG Knowledge Cards `CARD-004`, `CARD-005`, `CARD-006` and Phase 3 User Stories*

---

## 1. Crazy Eights Methodology & Design Rationale
In accordance with user experience design best practices, our design iterations explored **6–8 distinct layout concepts** across each of our 4 major application interfaces:
1. **Screen S-01: Home Vertical Discovery Stream** (Passive consumption, swipe gestures, video auto-play).
2. **Screen S-02: Consultant Bento Grid Profile** (5-second due diligence audit, verified authority baseline).
3. **Screen S-03: 4-Step Creation Studio** (Split-screen authoring, narrative templates, anti-clutter rules).
4. **Screen S-04: Native Slide-Up Booking & Escrow Sheet** (Zero-redirect scheduling, M-Pesa STK push, milestone locker).

Below are the synthesized, high-fidelity ASCII/Markdown wireframes with complete GUI widget input and output annotations.

---

## 2. Screen S-01: Home Vertical Discovery Stream

```
+---------------------------------------------------------------+
| [Logo: Consult Kenya]       [Q Search Hubs]      [Bell Alerts] |
+---------------------------------------------------------------+
|                                                               |
|  +---------------------------------------------------------+  |
|  | [@leah_systems] [Silver Verified] [CAS 8.9]  [Follow]   |  | (W-01)
|  | "M-Pesa B2C Payout Architecture for Micro-Insurers"     |  | (W-02)
|  +---------------------------------------------------------+  |
|  |                                                         |  |
|  |   +-------------------------------------------------+   |  |
|  |   | [SLIDE 2/5: System Architecture Diagram]        |   |  | (W-03)
|  |   |                                                 |   |  |
|  |   |   [Client App] --> [Daraja API] --> [Escrow]   |   |  |
|  |   |                        |                        |   |  |
|  |   |               [Redis Mutex Lock]                |   |  |
|  |   |                                                 |   |  |
|  |   | "Step 2: Guaranteeing 0-balance drift via      |   |  |
|  |   |  distributed Redis locks on Safaricom STK..."   |   |  |
|  |   +-------------------------------------------------+   |  |
|  |                                                         |  |
|  |   [o==o==o==o==o] Slide Progress Scrubber               |  | (W-04)
|  |                                                         |  |
|  |   [#SoftwareArchitecture] [#Fintech] [#Kenya]           |  | (W-05)
|  |                                                         |  |
|  |   +-------------------------------------------------+   |  |
|  |   | [CTA: Book 15-Min Architecture Audit (KES 20k)] |   |  | (W-06)
|  |   +-------------------------------------------------+   |  |
|  +---------------------------------------------------------+  |
|                                                               |
|  [Bookmark (5x)] (W-07)   [Share Deck] (W-08)   [Peer Endorse]| (W-09)
|                                                               |
+---------------------------------------------------------------+
| [Home (Active)]  [Explore]  [+] Publish  [Messages]  [Profile]| (W-10)
+---------------------------------------------------------------+
```

### Detailed Widget Annotations:
* **W-01 (Header Bar - Output & Input):** Displays author avatar, username, statutory verification badge (Silver), and live CAS score (`8.9`). Clicking avatar navigates to `Screen S-02` (Bento Grid Profile). Clicking `[Follow]` dispatches network subscription telemetry.
* **W-02 (Case Study Title - Output):** High-contrast headline summarizing the deliverable.
* **W-03 (Interactive Carousel Canvas - Output & Input):** Renders high-resolution vector diagrams and code syntax blocks. Horizontal touch drag ($>15\text{px}$) navigates slide-by-slide while temporarily locking vertical feed scrolling. Vertical swipe advances to next feed item.
* **W-04 (Slide Progress Scrubber - Output & Input):** Visual indicator showing current slide index (`Slide 2/5`). Tap on dots allows quick scrubbing between slides.
* **W-05 (Topic Hub Tags - Output & Input):** Clickable hashtags. Tapping `#Fintech` filters Explore view to that hub.
* **W-06 (Native Conversion Anchor - Input):** Sticky primary call-to-action button. Clicking slides up `Screen S-04` (In-App Booking Sheet) over the feed without navigating away.
* **W-07 (Bookmark Button - Input & Output):** Tapping saves post to user's library and dispatches a $5\times$ weighted telemetry boost to the author's CAS calculation pipeline.
* **W-08 (Share Deck Button - Input):** Generates deep-link targeting the current slide index or exports formatted PDF carousel for LinkedIn/Instagram.
* **W-09 (Peer Endorsement Button - Input):** Verified specialists can attach cryptographic peer attestations.
* **W-10 (5-Tab Global Navigation Bar - Input):** Persistent lower bar allowing instant macro-navigation between Home, Explore, Publish, Messages, and Profile.

---

## 3. Screen S-02: Consultant Bento Grid Profile (Due Diligence Mode)

```
+---------------------------------------------------------------+
| [< Back to Feed]       [Consultant Profile]          [Share]  |
+---------------------------------------------------------------+
|  [Avatar]  Leah Wanjiku, MSc                [Book Me] (W-11) |
|            Lead Systems Architect & LSK Mediator              |
|            [Silver Verified]  [CAS: 9.15/10.0]  [Rating 4.9★] | (W-12)
|                                                               |
|  "Helping SACCOs and FinTechs scale to 100k daily txns."      |
|  Hourly Advisory: KES 15,000 | Nairobi, Kenya | English/Swa   |
+---------------------------------------------------------------+
|  View: [● Visual Bento Grid]  [○ Chronological Feed]          | (W-13)
+---------------------------------------------------------------+
|  +-----------------------------+ +--------------------------+ |
|  | FLAGSHIP CASE STUDY (W-14)  | | STATUTORY BADGE (W-15)   | |
|  | "Core SACCO CBS Migration"  | | [LSK Roll #14285]        | |
|  | [10-Slide Interactive Deck] | | Valid Through Dec 2026   | |
|  | 420 Saves | 18 Contracts    | | [View Registry Record]   | |
|  +-----------------------------+ +--------------------------+ |
|  +-----------------------------+ +--------------------------+ |
|  | VERIFIED CODE REPO (W-16)   | | CLIENT TESTIMONIAL(W-17) | |
|  | [GitHub: daraja-mpesa-sdk]  | | "Flawless audit of our   | |
|  | ★ 340 Stars | 120 Commits   | |  payment gateway."       | |
|  | Language: Python / Go       | | - David K., CTO (FinCo)  | |
|  +-----------------------------+ +--------------------------+ |
|  +----------------------------------------------------------+ |
|  | ACTIVE RETAINER PACKAGES: [KES 150k/mo SACCO Retainer]   | | (W-18)
|  +----------------------------------------------------------+ |
+---------------------------------------------------------------+
| [Home]     [Explore]     [+] Publish     [Messages]  [Profile]|
+---------------------------------------------------------------+
```

### Detailed Widget Annotations:
* **W-11 (Header CTA - Input):** High-priority sticky button launching native booking sheet.
* **W-12 (Authority Summary Block - Output):** Displays statutory verification badges, aggregate star rating ($4.9\star$), and calculated CAS score ($9.15$). Clicking badge shows cryptographic proof.
* **W-13 (Contextual View Toggle - Input):** Sub-toggle switching between high-density Bento Grid and chronological post timeline without page reload.
* **W-14 (Flagship Case Study Tile - Input & Output):** Prominent rectangular tile showcasing top deliverable. Tapping opens full-screen interactive case study overlay.
* **W-15 (Statutory Credential Tile - Input & Output):** Interactive tile verifying Law Society of Kenya / ICPAK registration standing. Tapping opens modal with verification timestamp and licensing board identifier.
* **W-16 (Developer Proof Tile - Input & Output):** GitHub API live widget showing verified repository stats, commit hashes, and language breakdown.
* **W-17 (Client Testimonial Tile - Output):** Enterprise sign-off quote with verified client company badge.
* **W-18 (Retainer Package Tile - Input):** Direct commercial contract hook allowing clients to initiate ongoing advisory agreements.

---

## 4. Screen S-03: 4-Step Creation Studio (Split-Screen Desktop Mode)

```
+-------------------------------------------------------------------------------+
| [X Cancel]                 CONSULT KENYA CREATION STUDIO        [Save Draft]  |
+-------------------------------------------------------------------------------+
| STEP 1: Format   | STEP 2: Template* | STEP 3: Evidence | STEP 4: Conversion  | (W-19)
+-------------------------------------------------------------------------------+
| [LEFT PANEL: Narrative Form Editor]           | [RIGHT: Live Mobile Preview]  |
|                                               |                               |
| Selected: [Template A: Case Study]            |   +-----------------------+   |
|                                               |   | [@leah] [Preview]     |   |
| Slide 1: Challenge Definition (W-20)          |   |                       |   |
| [TextArea: High M-Pesa transaction latency...] |   | THE CHALLENGE         |   |
| Character Count: 185 / 300 Max [OK] (W-21)     |   | High M-Pesa latency   |   |
|                                               |   | causing 12% dropped   |   |
| Slide 2: Technical Architecture (W-22)        |   | checkouts in SACCOs.  |   |
| [TextArea: Mermaid Diagram or Code Snippet...] |   |                       |   |
| ```mermaid                                     |   | [Architecture Schema] |   |
| flowchart LR; Client-->Gateway-->DB;           |   | [Verified GitHub Pill]|   |
| ```                                           |   |                       |   |
|                                               |   | [Book Consultation]   |   |
| Slide 3: Measurable Business Impact           |   +-----------------------+   |
| [TextArea: Reduced dropped txns to <0.1%...]  | (W-23: Instant Live Sync)     |
|                                               |                               |
| [+ Add Supporting Slide] (W-24)               |                               |
|                                               |                               |
| [Attach GitHub Commit / URL] (W-25)           |                               |
| [Redact Sensitive IP / Blur Tool] (W-26)      |                               |
+-------------------------------------------------------------------------------+
| [< Previous Step]                              [Next Step: Conversion Hook >] | (W-27)
+-------------------------------------------------------------------------------+
```

### Detailed Widget Annotations:
* **W-19 (Progress Stepper - Output & Input):** 4-step wizard indicator (*Format $\to$ Template $\to$ Evidence $\to$ Conversion*). Tapping completed steps allows rapid jumping.
* **W-20 (Narrative Slide Field - Input):** Structured text box pre-configured for the selected template (*Challenge $\to$ Solution $\to$ Impact*).
* **W-21 (Character Counter & Gate - Output):** Real-time counter enforcing maximum 300 characters per slide. If $>300$, border turns red and next button is disabled.
* **W-22 (Code & Architecture Canvas - Input):** Specialized input supporting markdown, language-specific syntax highlighting, and Mermaid.js vector diagram rendering.
* **W-23 (Live Mobile Preview Pane - Output):** Real-time interactive phone emulator rendering the exact slide layout, font sizes, and contrast as typed.
* **W-24 (Add Slide Button - Input):** Appends an additional structured slide up to a maximum of 10 slides per carousel.
* **W-25 (Proof Attachment Field - Input):** Input for GitHub repo URL, commit SHA, or public PDF audit whitepaper.
* **W-26 (In-Studio Redaction Blur Tool - Input):** Canvas utility allowing the creator to click-and-drag over proprietary IP names, account numbers, or hostnames to permanently blur them before upload.
* **W-27 (Navigation Footer Buttons - Input):** Advances through wizard with validation checks.

---

## 5. Screen S-04: Native Slide-Up Booking & Escrow Sheet

```
+---------------------------------------------------------------+
| [===== Drag Handle =====]                           [X Close] |
|                  SCHEDULE ADVISORY CONSULTATION                |
|                  with Leah Wanjiku (KES 15,000)                |
+---------------------------------------------------------------+
| STEP 1: Select Date & Time (Local Time: EAT GMT+3) (W-28)     |
|   < October 2026 >                                            |
|   [Mon 12]  [Tue 13]  [Wed 14*]  [Thu 15]  [Fri 16]           |
|                                                               |
|   Available Slots:                                            |
|   [ 09:00 AM ]  [ 11:30 AM (Selected)* ]  [ 02:00 PM ]        |
|   (Slot held for 10:00 minutes upon checkout)                 | (W-29)
+---------------------------------------------------------------+
| STEP 2: Project Intake Questions (Mandatory) (W-30)           |
|   1. What is the primary architecture challenge?              |
|      [TextArea: High transaction latency during STK push...]  |
|   2. Current technology stack: [Node.js, PostgreSQL, Daraja]   |
|   3. Expected deliverable: [Audit Report & Remediation Plan]  |
+---------------------------------------------------------------+
| STEP 3: Payment Method (W-31)                                 |
|   (*) M-Pesa STK Push      ( ) Credit / Debit Card (USD/EUR)  |
|                                                               |
|   Safaricom Phone Number: [ 0712 345 678 ]                    |
|   Amount: KES 15,000 (Incl. VAT)                              |
+---------------------------------------------------------------+
| [ CONFIRM & SEND M-PESA STK PROMPT (KES 15,000) ] (W-32)      |
+---------------------------------------------------------------+
| [Lock Icon] Funds held securely in Consult Kenya Escrow Trust |
+---------------------------------------------------------------+
```

### Detailed Widget Annotations:
* **W-28 (Calendar Slot Grid - Input & Output):** Interactive calendar rendering open 30-minute slots normalized to client local time zone with consultant working hour buffers.
* **W-29 (Mutex Reservation Badge - Output):** Notification showing active 10-minute lock on chosen slot to prevent race-condition double bookings.
* **W-30 (Intake Question Form - Input):** Mandatory 3-question project questionnaire. Validation requires all fields to be populated before checkout button unlocks.
* **W-31 (Payment Rail Selector - Input):** Radio button toggling between M-Pesa STK Push and International Multi-Currency Card Rails (with live CBK FX rate display).
* **W-32 (Checkout Action Button - Input):** Dispatches STK push payload to client mobile handset and starts 60-second animated PIN countdown timer.
