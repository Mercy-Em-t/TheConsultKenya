/**
 * Consult Kenya - Problem-Fit Customer Discovery Survey Generator
 * Powered by google-form-survey-suite
 *
 * HOW TO EXECUTE:
 * 1. Open your browser and navigate to https://script.google.com
 * 2. Click "New Project".
 * 3. Delete any default code in the editor and paste this entire script.
 * 4. Click the "Save" icon (diskette), then select "buildProblemDiscoverySurvey" and click "Run".
 * 5. Review authorizations when prompted by Google.
 * 6. Check the "Execution Log" at the bottom of the screen to copy your live Form URL and Edit URL!
 */

function buildProblemDiscoverySurvey() {
  var form = FormApp.create("Consult Kenya: Problem Discovery & Customer Pain Study");
  form.setDescription(
    "A research study on how enterprise buyers, founders, and independent specialists in Kenya " +
    "discover technical expertise, evaluate competence, and manage advisory contract risks.\n\n" +
    "Strictly non-pitch. Focused purely on understanding your past experiences."
  );

  // Section 1: Demographics
  form.addSectionHeaderItem()
    .setTitle("Section 1: Background & Role")
    .setHelpText("Your current professional capacity.");

  var roleItem = form.addMultipleChoiceItem();
  roleItem.setTitle("What best describes your primary professional role?")
    .setChoiceValues([
      "Enterprise Executive (CTO, CIO, Legal Counsel, CFO)",
      "Startup Founder / SME Business Owner",
      "Independent Technical Specialist / Consultant",
      "Corporate Procurement / Vendor Lead",
      "Regulated Professional (Advocate, CPA-K, PEng)"
    ])
    .setRequired(true);

  // Section 2: Problem Discovery
  form.addPageBreakItem()
    .setTitle("Section 2: Verifying Competence (The Resume Problem)");

  var qLinkedIn = form.addScaleItem();
  qLinkedIn.setTitle("On a scale of 1 to 5, how useful do you find traditional LinkedIn profiles and text resumes for verifying actual technical delivery competence?")
    .setBounds(1, 5)
    .setLabels("1 = Completely Useless / Fluff", "5 = Highly Reliable & Definitive")
    .setRequired(true);

  var qFormat = form.addMultipleChoiceItem();
  qFormat.setTitle("When evaluating an external specialist's past work, which evidence format gives you the highest confidence in their competence?")
    .setChoiceValues([
      "Swipeable visual case study / architecture map showing Challenge -> Solution -> Impact",
      "Live GitHub code repository or verified technical commit log",
      "Formal 50-page text whitepaper or PDF report",
      "Personal reference phone call with a mutual contact",
      "Standard list of past job titles on a CV"
    ])
    .setRequired(true);

  // Section 3: Escrow & Payment
  form.addPageBreakItem()
    .setTitle("Section 3: Contracting, Disputes & Escrow");

  var qPayment = form.addMultipleChoiceItem();
  qPayment.setTitle("For short advisory sessions (e.g., 30-min architecture review), how do you prefer to pay or receive fees?")
    .setChoiceValues([
      "Instant M-Pesa STK Push directly on mobile",
      "Corporate Credit / Debit Card (Visa / Mastercard)",
      "Manual Bank Wire (EFT / RTGS) with formal invoice"
    ])
    .setRequired(true);

  var qEscrow = form.addScaleItem();
  qEscrow.setTitle("How valuable would an automated milestone escrow system be, where client funds are locked upfront and only released upon formal deliverable sign-off?")
    .setBounds(1, 5)
    .setLabels("1 = Not Valuable", "5 = Essential / Non-Negotiable")
    .setRequired(true);

  var publishedUrl = form.getPublishedUrl();
  var editUrl = form.getEditUrl();

  Logger.log("=================================================");
  Logger.log("PROBLEM DISCOVERY SURVEY CREATED SUCCESSFULLY!");
  Logger.log("Live Form URL: " + publishedUrl);
  Logger.log("Edit Form URL: " + editUrl);
  Logger.log("=================================================");
}
