import os

base_dir = r"c:\Users\user\Documents\KenyaConsult\sad_phase3_ui_design"
scenarios_dir = os.path.join(base_dir, "scenarios")
messages_dir = os.path.join(base_dir, "messages")
prototypes_dir = os.path.join(base_dir, "prototypes")

os.makedirs(scenarios_dir, exist_ok=True)
os.makedirs(messages_dir, exist_ok=True)
os.makedirs(prototypes_dir, exist_ok=True)

# -------------------------------------------------------------
# 1. SCENARIOS GENERATION
# -------------------------------------------------------------
use_scenarios = [
    {
        "id": "SCEN-01",
        "title": "Enterprise CTO Discovers & Books a Fintech Compliance Specialist",
        "persona": "David Mutua, CTO at a Nairobi Tier-2 Commercial Bank",
        "goal": "Audit internal core-banking middleware against KRA eTIMS statutory specifications in under 48 hours.",
        "preconditions": "David accesses Consult Kenya on his iPhone 15 Pro via Safari over Safaricom 5G during an executive commute.",
        "steps": [
            "1. Lands on Home Feed; perceives immediate high-contrast vertical stream of case studies.",
            "2. Swipes up twice, spotting a verified case study: 'eTIMS Phase 2 Core Banking Migration (KES 40M Tax Exposure Resolved)'.",
            "3. Taps card to inspect split-screen Mermaid architecture diagram comparing legacy API vs. modern resilient queuing.",
            "4. Clicks the author avatar (@wanjiku_architect) to open her Bento Grid profile; observes Tier 3 Authority Badge, ICPAK verification seal, and 100% escrow completion rate.",
            "5. Taps sticky CTA: 'Book 45-Min Architecture Audit - KES 15,000'.",
            "6. Calendar sheet slides up; selects tomorrow at 2:00 PM EAT; inputs bank middleware briefing in 3 text boxes.",
            "7. Selects 'Pay via M-Pesa STK Push'; receives prompt on handset within 2 seconds; inputs PIN.",
            "8. Interface displays verified booking confirmation with encrypted WebRTC link and Google Calendar sync token."
        ],
        "ux_implications": "Requires zero-friction vertical swiping, sub-second Bento profile transitions, and seamless M-Pesa push without leaving the booking drawer."
    },
    {
        "id": "SCEN-02",
        "title": "Specialist Architect Authors Visual Case Study in Creation Studio",
        "persona": "Wanjiku Karanja, Lead Cloud & Security Architect",
        "goal": "Document a real-world AWS-to-Azure hybrid cloud migration with proof of execution to generate high-ticket advisory leads.",
        "preconditions": "Wanjiku is logged in on a MacBook Pro (16-inch display) in her Nairobi office.",
        "steps": [
            "1. Clicks '+ Create Case Study' in top navigation bar; system opens split-screen Creation Studio canvas.",
            "2. Selects 'Technical Architecture Blueprint' template; canvas pre-populates structured sections: Challenge, Blueprint, Execution, Impact.",
            "3. Enters markdown text in left editor; types Mermaid flowchart syntax for dual-region failover topology.",
            "4. Right preview pane compiles and renders interactive SVG diagram in real time with syntax error highlighting.",
            "5. Navigates to 'Evidence & Proof' tab; pastes GitHub commit link and uploads sanitized architecture PDF; system verifies hash via GitHub API and badges proof.",
            "6. Configures Conversion Anchor CTA: 'Book 1-on-1 Advisory Call - KES 20,000 / 60 Mins'.",
            "7. Clicks 'Publish'; automated DLP scanner confirms zero unredacted IP or credentials; deck enters public feed with Tier 3 CAS boost."
        ],
        "ux_implications": "Demands two-column split-screen layout, live SVG compile feedback, intuitive proof drag-and-drop, and non-blocking background auto-saving every 30 seconds."
    },
    {
        "id": "SCEN-03",
        "title": "Corporate Buyer Funds & Approves Escrow Milestone Deliverable",
        "persona": "Amina Hassan, Head of Procurement at an East African Logistics Conglomerate",
        "goal": "Review a delivered customs clearance automation blueprint and disburse KES 250,000 milestone funds.",
        "preconditions": "Amina receives an SMS and email notification that Milestone 2 has been submitted by the consultant.",
        "steps": [
            "1. Taps deep link in email on her iPad; authenticates via FaceID into the Escrow Management portal.",
            "2. Milestone dashboard displays 72-hour inspection countdown timer with amber status indicator.",
            "3. Inspects submitted artifacts (ZIP archive, SHA-256 fingerprint, and deployment URL) in the inline file previewer.",
            "4. Verifies deliverable against SOW acceptance criteria checklist.",
            "5. Clicks green primary button: 'Approve Milestone & Release Funds'.",
            "6. Confirmation modal summarizes financial settlement: Milestone Total (KES 250,000), 7% Platform Fee (KES 17,500), Net Consultant Payout (KES 232,500), and KRA Withholding Tax deduction.",
            "7. Enters SMS OTP verification code; system displays green success checkmark, generates KRA eTIMS invoice with QR code, and triggers M-Pesa B2C payout."
        ],
        "ux_implications": "Critical financial transparency: fee deductions must be unmistakably clear; irreversible approval actions must require explicit 2FA modal confirmation."
    },
    {
        "id": "SCEN-04",
        "title": "Escrow Dispute Mediation & Legal Adjudication",
        "persona": "Senior Counsel Otieno, Appointed Platform Escrow Mediator",
        "goal": "Adjudicate an unresolvable scope dispute between an enterprise client and a consultant for Milestone 3.",
        "preconditions": "Otieno logs into the Mediator Adjudication Workspace on desktop Chrome.",
        "steps": [
            "1. Opens 'Dispute Queue'; selects Case #DISP-2026-088; escrow balance is displayed as FROZEN (KES 180,000).",
            "2. Interface presents three-pane legal workspace: Left (SOW Contract & Acceptance Clauses), Center (Delivered Code Artifacts & Commit History), Right (Client Claim vs. Consultant Rebuttal Dossier).",
            "3. Otieno uses the interactive diff tool to identify that 3 out of 5 required endpoints were implemented to specification.",
            "4. Navigates to 'Adjudication Verdict' tab; selects 'Prorated Settlement'; adjusts slider to 60% Consultant (KES 108,000) and 40% Client Refund (KES 72,000).",
            "5. Inputs legal rationale citing Contract Clause 8.2 in the formatted decision text box.",
            "6. Digitally signs ruling using hardware security key; system unfreezes escrow, executes disbursement, and generates sealed Adjudication Certificate PDF."
        ],
        "ux_implications": "Three-pane dense legal layout, synchronized scrolling across contract and diffs, and precise numeric percentage sliders with instant currency recomputation."
    }
]

# Write scenario files
for sc in use_scenarios:
    sc_path = os.path.join(scenarios_dir, f"{sc['id']}_{sc['title'].replace(' ', '_').replace('&', 'And')[:50]}.md")
    lines = [
        f"# User Scenario: {sc['title']}",
        f"**Scenario ID:** `{sc['id']}` | **Persona:** {sc['persona']}\n",
        f"### Business Goal\n{sc['goal']}\n",
        f"### Initial Preconditions & Environmental Context\n{sc['preconditions']}\n",
        "### Step-by-Step User Interaction Narrative",
        "\n".join(sc['steps']),
        f"\n### UI / UX Ergonomic Implications\n{sc['ux_implications']}"
    ]
    with open(sc_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# Write scenarios index
with open(os.path.join(scenarios_dir, "INDEX.md"), "w", encoding="utf-8") as f:
    f.write("# Master User Scenarios Catalog\n\n")
    f.write("| ID | Scenario Title | Target Persona | Key Ergonomic Implication |\n")
    f.write("| :--- | :--- | :--- | :--- |\n")
    for sc in use_scenarios:
        f.write(f"| **{sc['id']}** | {sc['title']} | {sc['persona']} | {sc['ux_implications'][:80]}... |\n")

print(f"Generated {len(use_scenarios)} scenario files in {scenarios_dir}")

# -------------------------------------------------------------
# 2. MESSAGES GENERATION (Status, Confirmation, Warning, Error)
# -------------------------------------------------------------
messages_data = [
    {
        "id": "MSG-STATUS-01",
        "type": "Status / Informational Message",
        "trigger": "User initiates case study drafting or asynchronous task (e.g. background save, vector re-indexing).",
        "visual_style": "Subtle non-blocking toast at bottom-right (Desktop) or top pill (Mobile); blue/neutral palette (#2563EB).",
        "copy": "Draft saved automatically. All diagrams and assets synced.",
        "dismissal": "Auto-dismisses after 3 seconds; no user action required."
    },
    {
        "id": "MSG-CONFIRM-01",
        "type": "Confirmation Message",
        "trigger": "User is about to execute an irreversible action (e.g., releasing escrow funds, cancelling a booking, deleting a case study).",
        "visual_style": "Centrally focused modal dialog with dark backdrop blur; clear typography; high-contrast action buttons.",
        "copy": "Are you sure you want to approve Milestone 2 and release KES 250,000? This action is legally binding and irreversible.",
        "dismissal": "Requires explicit button click: Primary 'Yes, Authorize Release' (Green) or Secondary 'Cancel' (Neutral Gray)."
    },
    {
        "id": "MSG-WARNING-01",
        "type": "Warning Message",
        "trigger": "Approaching critical thresholds (e.g., 72-hour inspection timer expiring in 6 hours, calendar slot hold expiring in 2 minutes).",
        "visual_style": "Amber alert banner (#D97706) pinned to top of viewport with countdown clock icon.",
        "copy": "Your 15-minute slot lock will expire in 2:00 minutes. Please complete payment to confirm your booking.",
        "dismissal": "Remains sticky until action is completed or timer expires."
    },
    {
        "id": "MSG-ERROR-01",
        "type": "Error / Recovery Message",
        "trigger": "Transactional or validation failure (e.g. M-Pesa STK timeout, invalid phone format, Mermaid syntax error).",
        "visual_style": "Red inline callout box (#DC2626) with exclamation triangle icon and explicit recovery instructions.",
        "copy": "M-Pesa payment prompt timed out on your phone. Please verify your phone is unlocked with network signal and click 'Retry STK Push', or switch to Card Payment.",
        "dismissal": "Persistent until user clicks recovery button ('Retry STK Push' or 'Select Card')."
    }
]

for msg in messages_data:
    m_path = os.path.join(messages_dir, f"{msg['id']}_{msg['type'].split(' ')[0]}.md")
    lines = [
        f"# System Message Specification: {msg['id']}",
        f"**Message Classification:** {msg['type']}\n",
        f"### When Displayed (Trigger)\n{msg['trigger']}\n",
        f"### Visual Presentation & Styling\n{msg['visual_style']}\n",
        f"### Canonical Copy & Text\n> **\"{msg['copy']}\"**\n",
        f"### Dismissal & User Action Protocol\n{msg['dismissal']}"
    ]
    with open(m_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

with open(os.path.join(messages_dir, "INDEX.md"), "w", encoding="utf-8") as f:
    f.write("# Master System Messages Catalog\n\n")
    f.write("| Message ID | Classification | Trigger Condition | Canonical Copy Preview |\n")
    f.write("| :--- | :--- | :--- | :--- |\n")
    for msg in messages_data:
        f.write(f"| **{msg['id']}** | {msg['type']} | {msg['trigger'][:60]}... | \"{msg['copy'][:60]}...\" |\n")

print(f"Generated {len(messages_data)} message specification files in {messages_dir}")

# -------------------------------------------------------------
# 3. INTERACTIVE HTML PROTOTYPE GENERATION
# -------------------------------------------------------------
html_prototype_code = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Consult Kenya - Interactive UI Prototype</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .bento-card { transition: all 0.2s ease-in-out; }
    .bento-card:hover { transform: translateY(-2px); }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between">

  <!-- TOP APP BAR -->
  <header class="sticky top-0 z-50 bg-slate-900/90 backdrop-blur-md border-b border-slate-800 px-4 py-3 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-500 to-cyan-500 flex items-center justify-center font-extrabold text-slate-950 text-lg shadow-lg shadow-emerald-500/20">CK</div>
      <div>
        <h1 class="font-bold text-base tracking-tight leading-none">Consult Kenya</h1>
        <span class="text-xs text-emerald-400 font-medium">Authority & Advisory Network</span>
      </div>
    </div>
    <div class="flex items-center gap-2">
      <button class="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition" title="Search Topic Hubs"><i data-lucide="search" class="w-5 h-5"></i></button>
      <button class="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition" title="Notifications"><i data-lucide="bell" class="w-5 h-5"></i></button>
      <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-amber-400 to-orange-500 flex items-center justify-center text-xs font-bold text-slate-950 cursor-pointer">DM</div>
    </div>
  </header>

  <!-- MAIN VIEWPORT (DUAL-MODE FEED & BENTO SHOWCASE) -->
  <main class="flex-1 max-w-4xl w-full mx-auto p-4 space-y-6">

    <!-- FEED MODE TOGGLE & TOPIC CHIPS -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div class="flex items-center bg-slate-900 p-1 rounded-xl border border-slate-800 self-start">
        <button id="btnVertical" onclick="switchMode('vertical')" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-500 text-slate-950 transition flex items-center gap-1.5"><i data-lucide="smartphone" class="w-3.5 h-3.5"></i> Vertical Stream</button>
        <button id="btnBento" onclick="switchMode('bento')" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-slate-200 transition flex items-center gap-1.5"><i data-lucide="layout-grid" class="w-3.5 h-3.5"></i> Bento Portfolio</button>
      </div>
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs">
        <span class="px-3 py-1 rounded-full bg-emerald-950/60 text-emerald-300 border border-emerald-800/60 font-medium cursor-pointer">#KRAeTIMS</span>
        <span class="px-3 py-1 rounded-full bg-slate-800 text-slate-300 hover:bg-slate-700 cursor-pointer">#FintechCore</span>
        <span class="px-3 py-1 rounded-full bg-slate-800 text-slate-300 hover:bg-slate-700 cursor-pointer">#CommercialLaw</span>
        <span class="px-3 py-1 rounded-full bg-slate-800 text-slate-300 hover:bg-slate-700 cursor-pointer">#CloudSecurity</span>
      </div>
    </div>

    <!-- VIEW 1: VERTICAL STREAM CARD -->
    <div id="viewVertical" class="space-y-6">
      <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl shadow-black/40">
        <!-- Author Header -->
        <div class="p-4 flex items-center justify-between border-b border-slate-800/60 bg-slate-900/50">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center font-bold text-white text-sm">WK</div>
            <div>
              <div class="flex items-center gap-1.5">
                <span class="font-bold text-sm">Wanjiku Karanja</span>
                <span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"><i data-lucide="badge-check" class="w-3 h-3 mr-0.5"></i> ICPAK Certified</span>
              </div>
              <p class="text-xs text-slate-400">Chief Cloud & Tax Systems Architect • CAS Score: 940 (Tier 3)</p>
            </div>
          </div>
          <button class="text-slate-400 hover:text-slate-200"><i data-lucide="bookmark" class="w-5 h-5"></i></button>
        </div>

        <!-- Case Content -->
        <div class="p-5 space-y-4">
          <div class="space-y-1">
            <span class="text-xs font-semibold text-emerald-400 uppercase tracking-wider">Production Architecture Case Study</span>
            <h2 class="text-lg font-bold text-white">eTIMS Phase 2 Core-Banking Middleware Integration</h2>
            <p class="text-xs text-slate-300 leading-relaxed">How we resolved a KES 40M statutory exposure by redesigning synchronous API calls into a zero-loss asynchronous queue topology with instant QR certification.</p>
          </div>

          <!-- Mermaid Visual Mock -->
          <div class="bg-slate-950 p-4 rounded-xl border border-slate-800/80 font-mono text-xs text-slate-300 space-y-2">
            <div class="text-[11px] text-slate-500 flex justify-between items-center border-b border-slate-800 pb-2">
              <span>SYSTEM ARCHITECTURE TOPOLOGY (MERMAID SVG)</span>
              <span class="text-emerald-400">Verified Execution Hash: 7c4e...89a1</span>
            </div>
            <div class="py-2 text-center text-slate-400">
              <div class="inline-block p-2 bg-slate-900 rounded border border-slate-700">Bank ERP Core</div>
              <span class="mx-2 text-emerald-400">&longrightarrow; [Celery Queue] &longrightarrow;</span>
              <div class="inline-block p-2 bg-slate-900 rounded border border-slate-700">eTIMS API Adapter</div>
              <span class="mx-2 text-emerald-400">&longrightarrow;</span>
              <div class="inline-block p-2 bg-emerald-950 rounded border border-emerald-600 text-emerald-300">KRA Registry QR</div>
            </div>
          </div>

          <!-- Proof Badges -->
          <div class="flex flex-wrap items-center gap-2 pt-1 text-xs">
            <span class="px-2.5 py-1 rounded-lg bg-slate-800/80 text-slate-300 border border-slate-700/60 flex items-center gap-1.5"><i data-lucide="github" class="w-3.5 h-3.5 text-slate-400"></i> Commit: e8f921a</span>
            <span class="px-2.5 py-1 rounded-lg bg-slate-800/80 text-slate-300 border border-slate-700/60 flex items-center gap-1.5"><i data-lucide="file-check" class="w-3.5 h-3.5 text-emerald-400"></i> Audit Memo PDF</span>
            <span class="px-2.5 py-1 rounded-lg bg-emerald-950/40 text-emerald-300 border border-emerald-800/40 font-semibold ml-auto">Outcome: 99.99% Statutory Uptime</span>
          </div>
        </div>

        <!-- Sticky Conversion CTA Drawer -->
        <div class="p-4 bg-slate-900 border-t border-slate-800 flex items-center justify-between gap-4">
          <div>
            <div class="text-xs text-slate-400">Advisory Consultation</div>
            <div class="text-base font-extrabold text-white">KES 15,000 <span class="text-xs font-normal text-slate-400">/ 45 min session</span></div>
          </div>
          <button onclick="openBookingModal()" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 text-slate-950 font-bold text-xs hover:from-emerald-400 hover:to-teal-500 shadow-lg shadow-emerald-500/20 transition flex items-center gap-2">
            <i data-lucide="calendar" class="w-4 h-4"></i> Book In-App Consultation
          </button>
        </div>
      </div>
    </div>

    <!-- VIEW 2: BENTO GRID PROFILE -->
    <div id="viewBento" class="hidden space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Bento Tile 1: Profile & Bio -->
        <div class="md:col-span-2 bg-slate-900 border border-slate-800 p-5 rounded-2xl bento-card space-y-3">
          <div class="flex items-center gap-3">
            <div class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center font-extrabold text-white text-xl">WK</div>
            <div>
              <h2 class="text-lg font-bold">Wanjiku Karanja</h2>
              <p class="text-xs text-slate-400">Lead Cloud & Regulatory FinTech Architect</p>
              <div class="flex gap-2 mt-1">
                <span class="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-400 font-bold border border-emerald-500/20">LSK Verified</span>
                <span class="px-2 py-0.5 rounded text-[10px] bg-blue-500/10 text-blue-400 font-bold border border-blue-500/20">ICPAK Fellow</span>
              </div>
            </div>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">Specializing in high-throughput payment rails, KRA eTIMS statutory architecture, and enterprise cloud migrations across Kenya and East Africa.</p>
        </div>

        <!-- Bento Tile 2: CAS Rating Meter -->
        <div class="bg-gradient-to-br from-emerald-950/60 to-slate-900 border border-emerald-800/40 p-5 rounded-2xl bento-card flex flex-col justify-between">
          <div>
            <span class="text-xs text-emerald-400 font-semibold uppercase tracking-wider">Creator Authority</span>
            <div class="text-3xl font-extrabold text-white mt-1">940 <span class="text-sm font-normal text-slate-400">/ 1,000</span></div>
            <p class="text-[11px] text-slate-400 mt-1">Tier 3 Industry Authority (Top 1% across platform)</p>
          </div>
          <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden mt-4">
            <div class="bg-emerald-400 h-full w-[94%]"></div>
          </div>
        </div>

        <!-- Bento Tile 3: Completed Escrow Stats -->
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl bento-card space-y-1">
          <span class="text-xs text-slate-400">Escrow Milestone Track Record</span>
          <div class="text-2xl font-bold text-white">42 Completed</div>
          <div class="text-xs text-emerald-400 font-medium">100% On-Time Delivery • 0 Disputes</div>
        </div>

        <!-- Bento Tile 4: Booking Package -->
        <div class="md:col-span-2 bg-slate-900 border border-slate-800 p-5 rounded-2xl bento-card flex items-center justify-between">
          <div>
            <div class="text-xs text-slate-400">Direct Advisory Session</div>
            <div class="text-base font-bold text-white">45-Minute Technical Strategy Audit</div>
            <div class="text-xs text-emerald-400 font-medium">Next Available: Tomorrow, 2:00 PM EAT</div>
          </div>
          <button onclick="openBookingModal()" class="px-4 py-2.5 rounded-xl bg-emerald-500 text-slate-950 font-bold text-xs hover:bg-emerald-400 transition">Book Slot</button>
        </div>
      </div>
    </div>

  </main>

  <!-- BOTTOM NAVIGATION BAR -->
  <nav class="sticky bottom-0 z-40 bg-slate-900/95 backdrop-blur-md border-t border-slate-800 px-6 py-2.5 flex items-center justify-around text-slate-400 text-[10px] font-semibold">
    <button class="flex flex-col items-center gap-1 text-emerald-400"><i data-lucide="compass" class="w-5 h-5"></i><span>Discover</span></button>
    <button class="flex flex-col items-center gap-1 hover:text-slate-200 transition"><i data-lucide="layers" class="w-5 h-5"></i><span>Topic Hubs</span></button>
    <button class="flex flex-col items-center gap-1 hover:text-slate-200 transition"><i data-lucide="plus-circle" class="w-5 h-5 text-emerald-400"></i><span>Studio</span></button>
    <button class="flex flex-col items-center gap-1 hover:text-slate-200 transition"><i data-lucide="shield-check" class="w-5 h-5"></i><span>Escrow</span></button>
    <button class="flex flex-col items-center gap-1 hover:text-slate-200 transition"><i data-lucide="user" class="w-5 h-5"></i><span>Profile</span></button>
  </nav>

  <!-- MODAL: BOOKING & M-PESA CHECKOUT -->
  <div id="bookingModal" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 space-y-5 shadow-2xl">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h3 class="font-bold text-white text-base">Book Advisory Consultation</h3>
          <p class="text-xs text-slate-400">with Wanjiku Karanja (Tier 3 Specialist)</p>
        </div>
        <button onclick="closeBookingModal()" class="text-slate-400 hover:text-white"><i data-lucide="x" class="w-5 h-5"></i></button>
      </div>

      <!-- Slot Selection & Form -->
      <div class="space-y-3 text-xs">
        <div>
          <label class="block text-slate-300 font-semibold mb-1">Selected Calendar Slot</label>
          <div class="p-2.5 bg-slate-950 border border-slate-800 rounded-xl flex items-center justify-between text-slate-200 font-medium">
            <span>Tomorrow, Oct 24 • 2:00 PM - 2:45 PM EAT</span>
            <span class="text-[10px] text-amber-400 font-bold">15-min soft lock active</span>
          </div>
        </div>

        <div>
          <label class="block text-slate-300 font-semibold mb-1">Consultation Brief / Objective</label>
          <textarea rows="2" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-slate-200 placeholder-slate-600 focus:outline-none focus:border-emerald-500" placeholder="e.g. Audit core-banking middleware eTIMS compliance..."></textarea>
        </div>

        <div>
          <label class="block text-slate-300 font-semibold mb-1">Payment Rail</label>
          <div class="grid grid-cols-2 gap-2">
            <div class="p-2.5 rounded-xl border-2 border-emerald-500 bg-emerald-950/20 flex items-center gap-2 cursor-pointer font-bold text-white">
              <i data-lucide="smartphone" class="w-4 h-4 text-emerald-400"></i> M-Pesa STK
            </div>
            <div class="p-2.5 rounded-xl border border-slate-800 bg-slate-950 flex items-center gap-2 cursor-pointer text-slate-400">
              <i data-lucide="credit-card" class="w-4 h-4"></i> Credit / Card
            </div>
          </div>
        </div>

        <div>
          <label class="block text-slate-300 font-semibold mb-1">Safaricom Phone Number</label>
          <input type="text" value="+254 712 345 678" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-slate-200 font-mono font-medium focus:outline-none focus:border-emerald-500" />
        </div>
      </div>

      <!-- Action Button -->
      <div class="pt-2">
        <button onclick="triggerPayment()" class="w-full py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold text-xs hover:from-emerald-400 hover:to-teal-400 shadow-lg shadow-emerald-500/20 transition flex items-center justify-center gap-2">
          <span>Authorize M-Pesa STK Push (KES 15,000)</span>
        </button>
      </div>
    </div>
  </div>

  <script>
    lucide.createIcons();

    function switchMode(mode) {
      const v = document.getElementById('viewVertical');
      const b = document.getElementById('viewBento');
      const btnV = document.getElementById('btnVertical');
      const btnB = document.getElementById('btnBento');

      if (mode === 'vertical') {
        v.classList.remove('hidden');
        b.classList.add('hidden');
        btnV.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-500 text-slate-950 transition flex items-center gap-1.5';
        btnB.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-slate-200 transition flex items-center gap-1.5';
      } else {
        v.classList.add('hidden');
        b.classList.remove('hidden');
        btnB.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-500 text-slate-950 transition flex items-center gap-1.5';
        btnV.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-slate-200 transition flex items-center gap-1.5';
      }
    }

    function openBookingModal() {
      document.getElementById('bookingModal').classList.remove('hidden');
    }
    function closeBookingModal() {
      document.getElementById('bookingModal').classList.add('hidden');
    }
    function triggerPayment() {
      alert("Safaricom M-Pesa STK Push dispatched to +254 712 345 678! Check your phone to enter your PIN.");
      closeBookingModal();
    }
  </script>
</body>
</html>
"""

html_proto_path = os.path.join(prototypes_dir, "INTERACTIVE_UI_PROTOTYPE.html")
with open(html_proto_path, "w", encoding="utf-8") as f:
    f.write(html_prototype_code)

print(f"Generated standalone interactive HTML prototype in {html_proto_path}")
