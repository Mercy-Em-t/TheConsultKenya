# Scenario & Jackson-Zave Specification: UC-12

### UC-12: Conduct Secure Live Consultation
* **Requirement ($R_{12}$):** Clients and consultants must conduct confidential advisory sessions directly in the browser with encrypted audio/video and screen-sharing tools.
* **Specification ($S_{12}$):**
  * The machine shall establish an encrypted peer-to-peer WebRTC session via DTLS-SRTP, falling back to TURN relay servers if corporate firewalls block direct connection.
  * The machine shall support 1080p 30fps screen sharing.
  * The machine shall display a 5-minute remaining warning banner and provide an option to mutually extend the session by 15 minutes.
* **Assumption ($E_{12}$):**
  * Both participants possess functional webcams, microphones, and modern browsers (Chrome, Safari, Edge, Firefox).
* **Narrative Scenario ($SC_{12}$):**
  * *Context:* Kiprono and David enter their scheduled technical audit session.
  * *Execution:* Both click "Join Secure Room" inside Consult Kenya. Kiprono shares his screen to mark up David’s database architecture. At minute 25, a gentle banner reminds them of 5 minutes remaining. They conclude action items, wrap up at minute 30, and receive automated action-item notes via email.

---
