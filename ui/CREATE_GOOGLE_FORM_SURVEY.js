/**
 * Consult Kenya - Solution-Fit Customer Discovery Survey Generator
 * Powered by google-form-survey-suite
 *
 * HOW TO EXECUTE:
 * 1. Open your browser and navigate to https://script.google.com
 * 2. Click "New Project".
 * 3. Delete any default code in the editor and paste this entire script.
 * 4. Click the "Save" icon (diskette), then select "buildConsultKenyaSurvey" and click "Run".
 * 5. Review authorizations when prompted by Google.
 * 6. Check the "Execution Log" at the bottom of the screen to copy your live Form URL and Edit URL!
 */

function buildConsultKenyaSurvey() {
  var form = FormApp.create("Consult Kenya: Professional Advisory & Discovery Survey");
  form.setDescription(
    "A research study on how enterprise buyers, founders, and consultants in Kenya " +
    "discover technical expertise, evaluate professional competence, and de-risk advisory contracts.\n\n" +
    "All responses are strictly confidential under the Kenya Data Protection Act 2019."
  );

  // ==========================================
  // SECTION 1: DEMOGRAPHICS & PROFILE
  // ==========================================
  form.addSectionHeaderItem()
    .setTitle("Section 1: Professional Background & Role")
    .setHelpText("Tell us about your organization and how you interact with professional consultants.");

  var roleItem = form.addMultipleChoiceItem();
  roleItem.setTitle("What best describes your primary professional role?")
    .setChoiceValues([
      "Enterprise Executive / Director (CTO, CIO, Legal Counsel, CFO)",
      "Startup Founder / Business Owner",
      "Procurement / Vendor Management Lead",
      "Independent Technical Consultant / Specialist Architect",
      "Professional Services Firm Partner (Law, Tax, Engineering)"
    ])
    .setRequired(true);

  var companySize = form.addMultipleChoiceItem();
  companySize.setTitle("What is the size of your organization?")
    .setChoiceValues([
      "Solo Practitioner / Freelancer",
      "2 - 10 employees (Early Stage)",
      "11 - 50 employees (Growing SME)",
      "51 - 250 employees (Mid-Market)",
      "250+ employees (Enterprise / Multinational)"
    ])
    .setRequired(true);

  var locationItem = form.addMultipleChoiceItem();
  locationItem.setTitle("Where is your primary operational base?")
    .setChoiceValues([
      "Nairobi, Kenya",
      "Mombasa / Kisumu / Other Kenyan Urban Hub",
      "East Africa Region (Uganda, Tanzania, Rwanda)",
      "International / Diaspora"
    ])
    .setRequired(true);

  // ==========================================
  // SECTION 2: PROBLEM DISCOVERY (MOM-TEST APPROVED)
  // ==========================================
  form.addPageBreakItem()
    .setTitle("Section 2: Finding & Auditing External Consultants")
    .setHelpText("Reflect on your past experiences seeking specialized technical, legal, or financial expertise.");

  var qPastSearch = form.addParagraphTextItem();
  qPastSearch.setTitle("When was the last time you needed to hire an external consultant or technical specialist? How did you actually find them?")
    .setHelpText("Please walk us through the actual steps you took (e.g., asking on WhatsApp, LinkedIn search, personal network).")
    .setRequired(true);

  var qFrustration = form.addParagraphTextItem();
  qFrustration.setTitle("What was the hardest or most frustrating part about evaluating whether that consultant was truly competent before hiring them?")
    .setHelpText("Think about resumes, portfolios, or initial proposals you received.")
    .setRequired(true);

  var qLinkedInResumes = form.addScaleItem();
  qLinkedInResumes.setTitle("On a scale of 1 to 5, how useful do you find traditional LinkedIn profiles and text resumes for verifying actual technical delivery competence?")
    .setBounds(1, 5)
    .setLabels("1 = Completely Useless (Pure Fluff)", "5 = Extremely Reliable & Definitive")
    .setRequired(true);

  var qDeliverableFormat = form.addMultipleChoiceItem();
  qDeliverableFormat.setTitle("When evaluating a specialist's past work, which evidence format gives you the highest confidence in their competence?")
    .setChoiceValues([
      "A swipeable visual case study / architecture map showing Challenge -> Solution -> Impact",
      "A 50-page formal text whitepaper or PDF report",
      "A standard list of past job titles and company names on a CV",
      "A live GitHub code repository or verified technical commit log",
      "A personal reference phone call with a mutual contact"
    ])
    .setRequired(true);

  // ==========================================
  // SECTION 3: CONTRACTING, ESCROW & FINANCIAL SETTLEMENT
  // ==========================================
  form.addPageBreakItem()
    .setTitle("Section 3: Contracting, Escrow & Payment Rails")
    .setHelpText("How you handle financial commitments, milestones, and dispute risks.");

  var qEscrowExperience = form.addParagraphTextItem();
  qEscrowExperience.setTitle("Have you ever experienced a project where a consultant underdelivered, or a client delayed payment after work was submitted? What happened?")
    .setHelpText("Describe how the dispute or delay was resolved.")
    .setRequired(true);

  var qPaymentRail = form.addMultipleChoiceItem();
  qPaymentRail.setTitle("For short advisory sessions (e.g., 30-min architecture review or legal consult), how do you prefer to pay or receive fees?")
    .setChoiceValues([
      "Instant M-Pesa STK Push directly on mobile",
      "Corporate Credit / Debit Card (Visa / Mastercard)",
      "Manual Bank Wire (EFT / RTGS) with formal invoice",
      "Cash / Direct personal M-Pesa transfer"
    ])
    .setRequired(true);

  var qEscrowWillingness = form.addScaleItem();
  qEscrowWillingness.setTitle("How valuable would an automated milestone escrow system be, where client funds are locked upfront and only released upon formal deliverable sign-off?")
    .setBounds(1, 5)
    .setLabels("1 = Not Valuable (Prefer Direct Trust)", "5 = Essential (Must-Have for Projects > KES 100k)")
    .setRequired(true);

  var qFeedback = form.addParagraphTextItem();
  qFeedback.setTitle("Any additional thoughts on what a visual-first, authority-backed professional network in Kenya should prioritize?")
    .setRequired(false);

  // Output Links to Execution Log
  var publishedUrl = form.getPublishedUrl();
  var editUrl = form.getEditUrl();

  Logger.log("=================================================");
  Logger.log("CONSULT KENYA SURVEY CREATED SUCCESSFULLY!");
  Logger.log("Live Form URL: " + publishedUrl);
  Logger.log("Edit Form URL: " + editUrl);
  Logger.log("=================================================");
}
