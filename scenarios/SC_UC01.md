# Scenario & Jackson-Zave Specification: UC-01

### UC-01: Discover Content via Dual-Mode Feeds
* **Requirement ($R_{01}$):** Clients must be able to fluidly browse and absorb bite-sized professional engineering, legal, and financial frameworks without interface lag or video stutter.
* **Specification ($S_{01}$):**
  * The machine shall pre-render the next 2 feed cards in the background.
  * The machine shall transition between vertical cards with a $P_{95}$ latency $\le 200\text{ms}$.
  * The machine shall lock vertical feed gestures when horizontal touch drags $>15\text{px}$ are detected on a multi-slide carousel.
  * The machine shall automatically downgrade video streams to 70% quality WebP image slides when client downlink drops below $1\text{ Mbps}$.
* **Assumption ($E_{01}$):**
  * Client mobile hardware supports WebGL/CSS hardware acceleration.
  * Cellular telecom infrastructure in Kenya (Safaricom/Airtel) delivers at least intermittent 3G data speeds ($\ge 256\text{ kbps}$).
* **Narrative Scenario ($SC_{01}$):**
  * *Context:* David, a CTO in Nairobi, opens Consult Kenya on his iPhone while riding in an Uber along Waiyaki Way.
  * *Execution:* He swipes up on the Home feed. An engineering carousel breaking down an M-Pesa B2C retry architecture appears instantly. David swipes horizontally through slides 1 to 4. As the car enters a network dead-zone under a flyover, the video on the next card gracefully switches to crisp, lightweight WebP diagrams without crashing or stuttering.

---
