# Program Specification: EscrowDisputeAdjudicationEngine
**Program ID:** `PROG-08` | **Module Type:** Legal & Arbitration Domain Service
**Language / Framework:** `Python 3.12 / ReportLab PDF Engine / Cryptography`

### Description
Aggregates evidence dossiers (SOW clauses, git commits, delivery SHA-256 hashes), coordinates 48-hour counter-party rebuttals, computes prorated apportionment mathematics, and generates legally binding cryptographically signed Adjudication Certificate PDFs.

### Systems Design Characteristics
- **Cohesion Type:** Functional Cohesion (Dedicated arbitration analysis and dispute resolution)
- **Coupling Level:** Data Coupling
- **Fan-In:** `2` (High reuse by upstream callers)
- **Fan-Out:** `3` (Optimal controlled subordinate delegations)

### Associated Events & Triggers
- `EVT-DISPUTE-RAISED: Party halts milestone and requests mediation.`
- `EVT-RULING-SIGNED: Mediator signs binding apportionment decision.`

### Program Input Parameters
| Input Parameter | Data Transfer Object (DTO) | Internal Elements |
| :--- | :--- | :--- |
| **`dispute_submission`** | `DisputeSubmissionDTO` | milestone_id, reason_category, evidence_urls, claimant_id |
| **`mediator_ruling`** | `MediatorRulingDTO` | case_id, mediator_id, consultant_percent, client_percent, legal_rationale, hardware_sig |

### Program Output Returns
| Output Return | Data Transfer Object (DTO) | Internal Elements |
| :--- | :--- | :--- |
| **`dossier_packet`** | `DisputeDossierDTO` | case_id, contract_clauses, file_diffs, rebuttal_deadline |
| **`ruling_certificate`** | `RulingCertificateDTO` | certificate_pdf_url, disbursement_execution_id, closed_at |

### Detailed Algorithmic Pseudocode
```python
FUNCTION ExecuteAdjudicationRuling(case_id: UUID, ruling: MediatorRuling) -> RulingCertificate:
    INPUT: case_id, ruling (consultant_split_pct, client_split_pct, rationale, token_sig)
    OUTPUT: RulingCertificate (pdf_url, status)

    // 1. Verify Mediator Identity & Hardware Cryptographic Signature
    dispute_case = Database.DisputeCases.FindById(case_id)
    ASSERT dispute_case.status == "UNDER_ADJUDICATION"
    VerifyHardwareSignature(ruling.mediator_id, ruling.token_sig)

    // 2. Validate Apportionment Mathematics
    ASSERT (ruling.consultant_split_pct + ruling.client_split_pct) == 100.00
    milestone = Database.EscrowMilestones.FindById(dispute_case.milestone_id)
    escrow_principal = milestone.milestone_amount_kes

    consultant_share = escrow_principal * (ruling.consultant_split_pct / 100.0)
    client_share = escrow_principal * (ruling.client_split_pct / 100.0)

    // 3. Execute Dual Disbursement from Frozen Escrow
    BEGIN TRANSACTION
        IF consultant_share > 0 THEN
            SettlementEngine.DisburseNet(consultant_share, milestone.consultant_id, "DISPUTE_AWARD")
        END IF
        IF client_share > 0 THEN
            PaymentGateway.RefundClient(client_share, milestone.client_id, "DISPUTE_REFUND")
        END IF

        // 4. Generate Sealed Adjudication Certificate PDF
        pdf_bytes = LegalPDFEngine.GenerateCertificate(
            case_id=case_id,
            mediator_name=ruling.mediator_name,
            contract_id=milestone.contract_id,
            ruling_date=NOW(),
            consultant_awarded=consultant_share,
            client_refunded=client_share,
            rationale_text=ruling.legal_rationale
        )
        pdf_url = AmazonS3.PutObjectWithLock("legal-audit-vault/" + case_id + ".pdf", pdf_bytes)

        // Close Dispute Case
        Database.DisputeCases.CloseCase(case_id, pdf_url=pdf_url, closed_at=NOW())
        Database.EscrowMilestones.UpdateStatus(milestone.id, "CLOSED_DISPUTE_RESOLVED")
    COMMIT TRANSACTION

    RETURN RulingCertificate(pdf_url=pdf_url, status="RESOLVED_DISBURSED")
END FUNCTION
```
