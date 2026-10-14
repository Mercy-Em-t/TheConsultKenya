# System Message Specification: MSG-ERROR-01
**Message Classification:** Error / Recovery Message

### When Displayed (Trigger)
Transactional or validation failure (e.g. M-Pesa STK timeout, invalid phone format, Mermaid syntax error).

### Visual Presentation & Styling
Red inline callout box (#DC2626) with exclamation triangle icon and explicit recovery instructions.

### Canonical Copy & Text
> **"M-Pesa payment prompt timed out on your phone. Please verify your phone is unlocked with network signal and click 'Retry STK Push', or switch to Card Payment."**

### Dismissal & User Action Protocol
Persistent until user clicks recovery button ('Retry STK Push' or 'Select Card').