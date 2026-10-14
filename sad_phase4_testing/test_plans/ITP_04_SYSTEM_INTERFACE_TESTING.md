# INTEGRATION TEST PLAN: ITP-04 SYSTEM INTERFACE TESTING
**System:** Consult Kenya  
**Integration Category:** Tier 2 — System Interface Integration Testing  
**Test Objective:** Validate external third-party communication channels, API gateways, sandbox integrations, SSL/TLS handshake security, timeout resilience, and circuit-breaker failovers across all external systems: Safaricom Daraja, Kenya Revenue Authority (KRA) eTIMS OSCU, LiveKit Cloud WebRTC SFU, and Integrated Population Registration System (IPRS).  
**Target Systems:** Safaricom Daraja APIv2, KRA eTIMS Endpoint, LiveKit Cloud, IPRS Mock Gateway.  
**Minimum Required Test Scenarios:** 6 (Defined: 6).  

---

## Test Scenarios & Verification Matrix

| Scenario ID | External Interface Under Test | Interface Protocol & Contract | Injection Condition & Chaos Test | Expected Integration Behavior | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ITP04-SI-01** | **Safaricom Daraja STK Push Gateway** | HTTPS REST / JSON with OAuth2 Bearer Token + HMAC-SHA256. | Normal operation: Client initiates KES 10,000 checkout. | System authenticates with Daraja, formats STK Push, receives `CheckoutRequestID`, and waits for callback. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP04-SI-02** | **Safaricom Daraja Network Outage / Timeout** | Safaricom API drops connections or exceeds 15,000ms latency. | Latency injection: Daraja endpoint delayed by 18,000ms. | Circuit breaker trips after 3 consecutive timeouts. System fails gracefully to user ("M-Pesa services experiencing temporary delay, please retry in 60s") without thread pool exhaustion. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP04-SI-03** | **KRA eTIMS OSCU Signing API** | REST / XML / JSON with asymmetric RSA/ECDSA fiscal signature. | eTIMS invoice generation on milestone release (KES 50,000). | Payload marshaled into eTIMS schema. OSCU returns valid fiscal control code and cryptographic QR verification URL. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP04-SI-04** | **LiveKit Cloud WebRTC SFU Gateway** | WebRTC signaling over WSS (WebSocket Secure) + Token Auth. | Room creation for advisory session with 2 participants. | Consult Kenya backend issues HMAC-signed LiveKit access token with 70-minute TTL and restricted publishing grants. | _Pending — not yet executed_ | **NOT RUN** |
| **ITP04-SI-05** | **IPRS Identity Verification Interface** | SOAP / REST Government Gateway with Mutual TLS (mTLS). | New consultant verification: National ID `29384756`. | IPRS client connects using client certificate, verifies Kenyan citizen identity attributes (Full Name, DOB, Gender). | _Pending — not yet executed_ | **NOT RUN** |
| **ITP04-SI-06** | **Cloudflare Edge CDN & Turnstile Gateway** | HTTPS reverse proxy with Cloudflare Turnstile bot detection. | High-volume bot probe: 100 automated HTTP requests from headless crawler. | Cloudflare Turnstile blocks automated requests with HTTP 403 / Managed Challenge. Legitimate client requests pass through with valid token. | _Pending — not yet executed_ | **NOT RUN** |

---

## Pass / Fail Summary
- **Execution status:** NOT RUN. This plan has been designed but not yet executed.
- **Observed results:** to be recorded only from actual execution, with a link to the test run / CI job as evidence.
- **Coverage:** to be measured with `pytest --cov` when executed. No coverage figure has been measured yet.

> [!NOTE]
> An earlier version of this file showed observed results and coverage figures that were never measured. They were removed on 13 Oct 2026 (CR-2026-002).
