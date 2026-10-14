# Business Process Specification: Process Multi-Rail Payments & Escrow Ledger Accounting
**Process ID:** `PROC-5.0` | **Owner:** Client / Consultant / Safaricom Daraja / Bank Gateway

### Description
Executes payments via Safaricom M-Pesa STK Push, international 3D Secure cards, and RTGS wire transfers; locks funds into trust escrow; and manages double-entry ledger settlement.

### Associated External Entities
- **Client**
- **Consultant**
- **Safaricom M-Pesa Daraja Gateway**
- **Card Payment Processor (Paystack/Flutterwave)**
- **Commercial Settlement Bank**

### Associated Data Stores
- **D6: Bookings & Consultation Datastore**
- **D9: Immutable Escrow & Financial Ledger**
- **D2: Compliance & Audit Vault**

### Data Flow Analysis (Inputs & Outputs)
| Flow Direction | Data Flow Name / Payload | Source / Origin | Destination |
| :---: | :--- | :--- | :--- |
| $\longleftarrow$ (Inflow) | M-Pesa phone number & Payment initiation | Client | `PROC-5.0` |
| $\longleftarrow$ (Inflow) | Daraja STK push callback payload | Safaricom Gateway | `PROC-5.0` |
| $\longleftarrow$ (Inflow) | Tokenized card data & 3DS confirmation | Client / Card Processor | `PROC-5.0` |
| $\longleftarrow$ (Inflow) | RTGS wire settlement notification | Commercial Settlement Bank | `PROC-5.0` |
| $\longrightarrow$ (Outflow) | Daraja STK Push Request | `PROC-5.0` | Safaricom Daraja API |
| $\longrightarrow$ (Outflow) | Card Charge & 3DS Challenge | `PROC-5.0` | Card Processor API |
| $\longrightarrow$ (Outflow) | Double-Entry Escrow Lock Entry | `PROC-5.0` | D9: Escrow Ledger |
| $\longrightarrow$ (Outflow) | Payment Confirmation & Escrow Receipt | `PROC-5.0` | Client & Consultant |
| $\longrightarrow$ (Outflow) | Escrow State Update ('CONFIRMED_ESCROW_LOCKED') | `PROC-5.0` | D6: Bookings DB |

### Decomposed Sub-Processes (Level 1 DFD Scope)
| Sub-Process ID | Sub-Process Name | Operational Description |
| :---: | :--- | :--- |
| **5.1** | Initiate & Poll M-Pesa STK Push | Dispatches Lipa Na M-Pesa USSD prompt and processes callback. |
| **5.2** | Process Multi-Currency Card & 3DS Rails | Tokenizes card credentials and handles CBK exchange rate conversions. |
| **5.3** | Reconcile High-Value RTGS Bank Transfers | Issues Virtual Account Numbers (VAN) and processes bank settlement webhooks. |
| **5.4** | Maintain Double-Entry Escrow Ledger | Records segregated trust balances under immutable contract UUIDs. |
