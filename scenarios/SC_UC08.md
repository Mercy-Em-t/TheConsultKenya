# Scenario & Jackson-Zave Specification: UC-08

### UC-08: Verify Identity & Professional Credentials
* **Requirement ($R_{08}$):** The network must guarantee that every consultant offering commercial advisory services is verified against official government and professional registries.
* **Specification ($S_{08}$):**
  * The machine shall validate Kenyan National IDs and KRA PINs against IPRS/KRA gateways within $\le 60\text{s}$ to issue Bronze Verification.
  * The machine shall validate statutory professional board numbers (LSK, ICPAK, EBK) to issue Silver Verification and domain authority multipliers.
  * If an annual credential check fails or license revocation is reported, the machine shall immediately strip verification badges and place payouts on hold.
* **Assumption ($E_{08}$):**
  * Statutory professional boards maintain searchable, authoritative registries of practitioners in active legal standing.
* **Narrative Scenario ($SC_{08}$):**
  * *Context:* Otieno, an advocate of the High Court of Kenya, creates his consultant profile.
  * *Execution:* He submits his National ID and his Law Society of Kenya (LSK) roll number. Within 45 seconds, the automated check verifies his active practicing certificate. Otieno’s profile immediately gains a Silver Verified Seal, and his legal case studies are unlocked for feed distribution.

---
