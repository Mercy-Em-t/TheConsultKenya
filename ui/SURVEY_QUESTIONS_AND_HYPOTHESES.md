# Solution-Fit Customer Discovery Survey Questions & Falsifiable Hypotheses
*Generated via `google-form-survey-suite` for Consult Kenya*

---

## 1. Falsifiable Hypotheses & Pass/Fail Metrics

Before deploying our solution-fit customer interviews, we define three rigorous, falsifiable hypotheses:

### Hypothesis 1 (Customer & Problem Hypothesis):
* **Hypothesis:** Enterprise procurement managers, founders, and directors find traditional text resumes and LinkedIn profiles insufficient for verifying technical competence, actively desiring visual proof of past deliveries (*Challenge $\to$ Solution $\to$ Impact*).
* **Pass/Fail Metric:** **At least 7 out of 10 interviewees ($\ge 70\%$)** rate LinkedIn profiles $\le 2$ out of 5 for competence verification and state that visual case studies or code repos provide significantly higher confidence.

### Hypothesis 2 (Fintech & Booking Friction Hypothesis):
* **Hypothesis:** Clients abandon external scheduling links (Calendly, email chains) and prefer native, in-app scheduling powered by instant mobile M-Pesa STK push.
* **Pass/Fail Metric:** **At least 8 out of 10 interviewees ($\ge 80\%$)** select M-Pesa STK push or instant card payment over manual bank wires for sessions $< \text{KES } 50,000$.

### Hypothesis 3 (Milestone Escrow Value Hypothesis):
* **Hypothesis:** For multi-week advisory projects ($> \text{KES } 100,000$), both clients and independent consultants view milestone escrow protection (locked upfront, released on deliverable sign-off) as a non-negotiable trust requirement.
* **Pass/Fail Metric:** **At least 8 out of 10 interviewees ($\ge 80\%$)** rate the milestone escrow vault as $\ge 4$ out of 5 in necessity.

---

## 2. Interview Guide (Mom-Test Approved Questions)

### Section 1: Demographics & Operational Context
1. What best describes your primary professional role?
   * Enterprise Executive (CTO, CIO, Legal Counsel, CFO)
   * Startup Founder / SME Business Owner
   * Procurement / Vendor Management Lead
   * Independent Technical Consultant / Specialist Architect
   * Professional Services Firm Partner (Law, Tax, Engineering)
2. What is the size of your organization? (Solo, 2–10, 11–50, 51–250, 250+)
3. Where is your primary operational base? (Nairobi, Mombasa/Kisumu, East Africa Region, International/Diaspora)

### Section 2: Problem Discovery (Past Behavior Focus)
4. *When was the last time you needed to hire an external consultant or technical specialist? How did you actually find them?* (Focus on actual steps taken).
5. *What was the hardest or most frustrating part about evaluating whether that consultant was truly competent before hiring them?*
6. *On a scale of 1 to 5, how useful do you find traditional LinkedIn profiles and text resumes for verifying actual technical delivery competence?* (1 = Useless/Fluff, 5 = Highly Reliable).
7. *When evaluating a specialist's past work, which evidence format gives you the highest confidence in their competence?*
   * Swipeable visual case study / architecture map (*Challenge $\to$ Solution $\to$ Impact*)
   * 50-page formal text whitepaper or PDF report
   * Standard list of past job titles on a CV
   * Live GitHub code repository or verified technical commit log
   * Personal reference phone call with a mutual contact

### Section 3: Contracting, Escrow & Payment Rails
8. *Have you ever experienced a project where a consultant underdelivered, or a client delayed payment after work was submitted? What happened?*
9. *For short advisory sessions (e.g. 30-min architecture review), how do you prefer to pay or receive fees?* (M-Pesa STK, Corporate Card, Bank Wire, Direct Transfer).
10. *How valuable would an automated milestone escrow system be, where client funds are locked upfront and only released upon formal deliverable sign-off?* (Scale 1 to 5).
11. *Any additional thoughts on what a visual-first, authority-backed professional network in Kenya should prioritize?*

---

## 3. How to Deploy the Live Google Form
The automated Google Apps Script is generated and ready to run in [`ui/CREATE_GOOGLE_FORM_SURVEY.js`](file:///c:/Users/user/Documents/KenyaConsult/ui/CREATE_GOOGLE_FORM_SURVEY.js).

**Execution Steps:**
1. Open [Google Apps Script](https://script.google.com).
2. Click **New Project**.
3. Copy and paste the script code from [`ui/CREATE_GOOGLE_FORM_SURVEY.js`](file:///c:/Users/user/Documents/KenyaConsult/ui/CREATE_GOOGLE_FORM_SURVEY.js).
4. Click **Run** (`buildConsultKenyaSurvey`).
5. Check the **Execution Log** at the bottom to copy your live Form URL and begin gathering customer responses.
