# UC-22: Audit Financial Settlement & Tax Compliance
*Diagram Type: Data Flow Diagram (DFD Level 1 - Financial Audit & eTIMS Tax Engine)*

Traces fund distributions, automated 5–8% platform take rate accounting, KRA eTIMS invoice generation, and withholding tax certification.

```mermaid
flowchart LR
    EscrowVault[(Escrow Settlement Ledger)] -->|1: Milestone Release Trigger Event| AccountingEngine[Financial Settlement Engine]
    
    subgraph Revenue & Fee Calculation
        AccountingEngine -->|2: Calculate Platform Take Rate: 5%-8%| TakeRateCalc[Platform Fee Journalizer]
        AccountingEngine -->|3: Deduct Professional Withholding Tax: 5% WHT| WHTCalc[Statutory WHT Calculator]
        AccountingEngine -->|4: Compute Net Consultant Payout| NetPayoutCalc[Net Payout Router]
    end
    
    subgraph Internal Accounts
        TakeRateCalc -->|Platform Gross Revenue| OperatingAccount[(Company Operating Account)]
        NetPayoutCalc -->|Net Balance Credit| ConsultantWallet[(Consultant Payout Wallet)]
    end
    
    subgraph External Tax & Compliance Systems
        KRAeTIMS[KRA eTIMS Tax Gateway]
        CorporateClient((Corporate Client Finance))
        ConsultantUser((Consultant))
    end
    
    TakeRateCalc -->|5: Taxable Fee Payload| eTIMSService[Generate Electronic Tax Invoice]
    eTIMSService -->|6: Transmit Invoice Data| KRAeTIMS
    KRAeTIMS -->|7: Return Validated QR Code & Fiscal Signature| eTIMSService
    
    eTIMSService -->|8: Deliver eTIMS VAT Tax Invoice| CorporateClient
    WHTCalc -->|9: Generate Statutory WHT Certificate Slip| ConsultantUser
```
