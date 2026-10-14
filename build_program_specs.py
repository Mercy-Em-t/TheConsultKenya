import os

base_dir = r"c:\Users\user\Documents\KenyaConsult\sad_phase3_program_design"
programs_dir = os.path.join(base_dir, "programs")
os.makedirs(programs_dir, exist_ok=True)

# 8 Core Concrete Programs representing core backend modules
programs_data = [
    {
        "id": "PROG-01",
        "name": "AuthAndCredentialVerificationService",
        "module_type": "Control & Domain Service",
        "language_framework": "Python 3.12 / FastAPI / Pydantic v2",
        "description": "Authenticates user sessions via Argon2id and TOTP MFA, ingests professional credentials (National ID, KRA PIN, LSK/ICPAK/EBK license #), and executes automated queries against statutory government registry APIs.",
        "cohesion_type": "Functional Cohesion (Executes single, well-defined mathematical and verification tasks)",
        "coupling_level": "Data Coupling (Communicates strictly through typed DTO parameters)",
        "fan_in": 4, # Invoked by Mobile Gateway, Web Gateway, Admin Console, and Background Sync
        "fan_out": 3, # Calls UserRepo, AuditRepo, StatutoryRegistryClient
        "events": [
            "EVT-AUTH-LOGIN: User submits credentials or refresh token.",
            "EVT-AUTH-CRED-SUBMIT: Consultant submits professional license number for verification."
        ],
        "inputs": [
            ("login_request", "LoginDTO", "email, password_hash, otp_code"),
            ("credential_payload", "CredentialSubmissionDTO", "consultant_id, license_number, board_type, national_id")
        ],
        "outputs": [
            ("auth_token_pair", "TokenResponseDTO", "jwt_access_token (15m), refresh_token (7d)"),
            ("verification_result", "CredentialVerificationResultDTO", "status, verified_at, registry_hash, new_tier")
        ],
        "pseudocode": """FUNCTION VerifyProfessionalLicense(consultant_id: UUID, board_type: Enum, license_no: String) -> CredentialResult:
    INPUT: consultant_id, board_type, license_no
    OUTPUT: CredentialResult (status, registry_hash, timestamp)

    // 1. Validate Input Format
    IF NOT MatchesPattern(license_no, BoardRegexPattern(board_type)) THEN
        RAISE ValidationError("Invalid license format for " + board_type)
    END IF

    // 2. Rate-Limiting & Idempotency Check
    token = Redis.GetLock("rate_limit:registry:" + consultant_id)
    IF token IS NULL THEN
        RAISE RateLimitException("Too many verification attempts. Please wait 5 minutes.")
    END IF

    // 3. Query Statutory Registry Adapter (e.g. LSK Advocate Roll, ICPAK Register)
    TRY
        registry_payload = StatutoryRegistryClient.QueryActiveStanding(board_type, license_no)
    CATCH TimeoutException:
        // Graceful circuit breaker fallback
        Database.Credentials.UpdateStatus(consultant_id, "PENDING_MANUAL_REVIEW")
        RETURN CredentialResult(status="PENDING_REVIEW", hash=NULL, timestamp=NOW())
    END TRY

    // 4. Verify Identity Match
    consultant = Database.Users.FindById(consultant_id)
    IF NormalizedName(consultant.full_name) == NormalizedName(registry_payload.full_name) AND registry_payload.is_active THEN
        computed_hash = SHA256(registry_payload.raw_response_bytes)
        
        // 5. Update Persistent DB State in Transaction
        BEGIN TRANSACTION
            Database.Credentials.Update(consultant_id, status="VERIFIED_ACTIVE", hash=computed_hash, verified_at=NOW())
            Database.ConsultantProfile.UpgradeAuthorityTier(consultant_id, "TIER_3_AUTHORITY")
            Database.AuditVault.LogVerificationEvent(consultant_id, board_type, license_no, computed_hash)
        COMMIT TRANSACTION
        
        // 6. Asynchronously trigger CAS score boost
        CeleryWorker.EnqueueTask("RecalculateCreatorAuthorityScore", consultant_id)
        
        RETURN CredentialResult(status="VERIFIED_ACTIVE", hash=computed_hash, timestamp=NOW())
    ELSE
        Database.Credentials.Update(consultant_id, status="REJECTED")
        RETURN CredentialResult(status="REJECTED", hash=NULL, timestamp=NOW())
    END IF
END FUNCTION"""
    },
    {
        "id": "PROG-02",
        "name": "CreationStudioMarkdownAndDiagramParser",
        "module_type": "Processing & Transformation Engine",
        "language_framework": "TypeScript / Node.js 20 & WebAssembly (Wasm)",
        "description": "Parses modular case study Markdown text, lints and compiles Mermaid syntax blocks into clean vector SVG strings, strips malicious XSS tokens, and verifies code syntax highlighting.",
        "cohesion_type": "Functional Cohesion (Transforms structured markup into sanitized SVG & HTML trees)",
        "coupling_level": "Data Coupling & Stamp Coupling (Accepts RawDraftDTO; returns CompiledCaseStudyDTO)",
        "fan_in": 3,
        "fan_out": 2, # Calls MermaidCompiler, HTMLSanitizer
        "events": [
            "EVT-STUDIO-KEYSTROKE: User types in Markdown split-screen editor.",
            "EVT-STUDIO-SAVE: User clicks save or 30-second background auto-save fires."
        ],
        "inputs": [
            ("raw_draft", "RawDraftDTO", "case_study_id, markdown_content, template_id")
        ],
        "outputs": [
            ("compiled_view", "CompiledViewDTO", "sanitized_html, svg_diagram_nodes, lint_errors_list")
        ],
        "pseudocode": """FUNCTION CompileCaseStudyDeck(raw_markdown: String) -> CompiledView:
    INPUT: raw_markdown
    OUTPUT: CompiledView (sanitized_html, svg_nodes, lint_errors)

    lint_errors = []
    svg_nodes = []

    // 1. Extract and Validate Mermaid Code Blocks
    diagram_blocks = RegexExtract(raw_markdown, /```mermaid([\\s\\S]*?)```/g)
    FOR EACH block IN diagram_blocks:
        TRY
            parsed_ast = MermaidParser.ParseSyntax(block.content)
            svg_string = MermaidRenderer.RenderToSVG(parsed_ast)
            svg_nodes.Append(ID=block.id, svg=svg_string)
        CATCH SyntaxError AS err:
            lint_errors.Append(Line=block.line_number, Message=err.message, Suggestion=err.fix_hint)
            // Render error placeholder box
            svg_nodes.Append(ID=block.id, svg=GenerateErrorPlaceholderSVG(err))
        END TRY
    END FOR

    // 2. Sanitize HTML & Prevent XSS Attacks
    sanitized_html = DOMPurify.Sanitize(MarkdownParser.ToHTML(raw_markdown), AllowedTags=["h1","h2","h3","p","code","pre","div","span"])

    // 3. Extract Meta Metrics (Dwell weights, readability score)
    word_count = CountWords(sanitized_html)
    estimated_read_time_seconds = word_count / 3.5

    RETURN CompiledView(
        html=sanitized_html,
        diagrams=svg_nodes,
        errors=lint_errors,
        read_time=estimated_read_time_seconds
    )
END FUNCTION"""
    },
    {
        "id": "PROG-03",
        "name": "TwoPassRecommendationAndCASRankingEngine",
        "module_type": "Algorithmic & AI Inference Service",
        "language_framework": "Python 3.12 / NumPy / pgvector / Redis",
        "description": "Executes the core algorithmic feed personalization: Pass 1 retrieves candidate case studies via Approximate Nearest Neighbor (ANN) vector cosine search; Pass 2 re-ranks candidates using weighted Creator Authority Scores (CAS) and anti-saturation diversity filters.",
        "cohesion_type": "Functional Cohesion (Mathematical vector dot-product and scoring pipeline)",
        "coupling_level": "Data Coupling (Input context vector, returns ranked list)",
        "fan_in": 2, # Web Feed Loader, Mobile Feed Loader
        "fan_out": 3, # pgvector DB, Redis Cache, Telemetry Sink
        "events": [
            "EVT-FEED-REQUEST: Client initiates discovery feed query.",
            "EVT-HOURLY-CRON: Batch daemon recalculates creator CAS multipliers."
        ],
        "inputs": [
            ("client_context", "ClientSessionContextDTO", "user_id, session_vector, geo_region, mode_preference")
        ],
        "outputs": [
            ("ranked_feed", "FeedResponseDTO", "top_20_cards, next_cursor, ranking_telemetry_id")
        ],
        "pseudocode": """FUNCTION GenerateTwoPassFeed(client_context: ClientContext) -> FeedResponse:
    INPUT: client_context (user_id, query_embedding, geo_tag)
    OUTPUT: FeedResponse (card_list, next_page_token)

    // PASS 1: Candidate Retrieval (ANN Vector Cosine Search)
    // Query top 200 candidates from pgvector using HNSW index
    candidates = Database.pgvector.CosineSimilarityQuery(
        vector=client_context.query_embedding,
        limit=200,
        filter_status="PUBLISHED"
    )

    // Retrieve pre-computed CAS scores from Redis in single MGET
    author_ids = ExtractUniqueAuthorIDs(candidates)
    cas_weights = Redis.MGet("cas_score:" + author_id FOR author_id IN author_ids)

    scored_candidates = []

    // PASS 2: Heavy Business Re-Ranking
    FOR EACH card IN candidates:
        author_cas = cas_weights.Get(card.author_id, DEFAULT=100.0) // 0 to 1000 scale
        norm_cas = author_cas / 1000.0
        
        geo_boost = 1.0
        IF card.target_region == client_context.geo_tag THEN
            geo_boost = 1.25 // 25% boost for Kenyan/East African localized content
        END IF

        freshness_decay = Math.Exp(-0.05 * DaysSince(card.published_at))

        // Composite Scoring Model
        composite_score = (card.cosine_similarity * 0.35) + 
                          (norm_cas * 0.40) + 
                          (geo_boost * 0.15) + 
                          (freshness_decay * 0.10)

        scored_candidates.Append(card, composite_score)
    END FOR

    // Sort descending by composite score
    SortDescending(scored_candidates, KEY=composite_score)

    // Diversity & Anti-Saturation Filter (Max 2 cards per author in top 20)
    top_20_feed = []
    author_counts = Map()

    FOR EACH item IN scored_candidates:
        author_count = author_counts.Get(item.author_id, 0)
        IF author_count < 2 THEN
            top_20_feed.Append(item.card)
            author_counts.Set(item.author_id, author_count + 1)
        END IF
        IF Length(top_20_feed) == 20 THEN
            BREAK
        END IF
    END FOR

    RETURN FeedResponse(cards=top_20_feed, cursor=GenerateCursor(top_20_feed.Last()))
END FUNCTION"""
    },
    {
        "id": "PROG-04",
        "name": "CalendarCoordinatorAndSlotLockManager",
        "module_type": "Concurrency & Coordination Service",
        "language_framework": "Python 3.12 / Redis 7.2 Distributed Locks",
        "description": "Coordinates real-time calendar availability synchronization across external providers (Google/Outlook) and enforces high-precision 15-minute temporary soft locks on advisory slots to prevent double-booking race conditions.",
        "cohesion_type": "Functional Cohesion (Atomic lock acquisition, renewal, and release)",
        "coupling_level": "Data Coupling",
        "fan_in": 3,
        "fan_out": 2, # Redis Cluster, Calendar API
        "events": [
            "EVT-SLOT-TAP: Client taps calendar time slot.",
            "EVT-LOCK-EXPIRE: 900 seconds elapse without confirmed payment."
        ],
        "inputs": [
            ("slot_request", "SlotLockRequestDTO", "client_id, consultant_id, slot_timestamp, duration_mins")
        ],
        "outputs": [
            ("lock_result", "SlotLockResponseDTO", "is_locked, lock_token, expires_at_timestamp")
        ],
        "pseudocode": """FUNCTION AcquireAdvisorySlotLock(client_id: UUID, consultant_id: UUID, start_time: Timestamp) -> LockResult:
    INPUT: client_id, consultant_id, start_time
    OUTPUT: LockResult (success, lock_token, expiry)

    lock_key = "slot_lock:" + consultant_id + ":" + FormatISO(start_time)
    lock_token = GenerateUUID()
    ttl_seconds = 900 // Exactly 15 minutes

    // Atomic Redis SET with NX (Set if Not Exists) and EX (Expiry)
    is_acquired = Redis.Set(lock_key, lock_token, NX=TRUE, EX=ttl_seconds)

    IF is_acquired THEN
        // Create pending booking draft record in PostgreSQL
        booking_id = Database.Bookings.InsertDraft(
            client_id=client_id,
            consultant_id=consultant_id,
            start_time=start_time,
            status="PENDING_PAYMENT",
            lock_token=lock_token
        )
        RETURN LockResult(success=TRUE, token=lock_token, expires_at=NOW() + 900)
    ELSE
        // Collision detected: Check if held by the same client
        current_holder = Redis.Get(lock_key)
        IF current_holder == lock_token THEN
            Redis.Expire(lock_key, ttl_seconds) // Refresh lock
            RETURN LockResult(success=TRUE, token=lock_token, expires_at=NOW() + 900)
        ELSE
            RETURN LockResult(success=FALSE, token=NULL, error="Slot currently reserved by another client")
        END IF
    END IF
END FUNCTION"""
    },
    {
        "id": "PROG-05",
        "name": "MpesaDarajaPaymentAndCallbackCoordinator",
        "module_type": "Fintech Transaction & Ingress Gateway",
        "language_framework": "Python 3.12 / FastAPI / Celery / Cryptography",
        "description": "Initiates Safaricom Lipa Na M-Pesa Online (STK Push) queries, validates incoming asynchronous webhook callback signatures, prevents duplicate replay attacks, and transitions booking and escrow states.",
        "cohesion_type": "Sequential Cohesion (Output of STK push initiation feeds directly into callback verification pipeline)",
        "coupling_level": "Data Coupling (Cryptographic callback JSON DTO)",
        "fan_in": 3,
        "fan_out": 4, # Safaricom API, DoubleEntryLedger, BookingDB, SMS Notification Service
        "events": [
            "EVT-PAY-MPESA-SUBMIT: Client clicks 'Pay via M-Pesa'.",
            "EVT-DARAJA-CALLBACK-POST: Safaricom gateway delivers transaction webhook."
        ],
        "inputs": [
            ("payment_init", "PaymentInitDTO", "booking_id, phone_number, amount_kes"),
            ("daraja_callback", "DarajaCallbackPayloadDTO", "MerchantRequestID, CheckoutRequestID, ResultCode, CallbackMetadata")
        ],
        "outputs": [
            ("stk_response", "STKPushResponseDTO", "CheckoutRequestID, ResponseCode, CustomerMessage"),
            ("reconciliation_status", "PaymentReconciliationDTO", "transaction_code, escrow_status, ledger_entry_id")
        ],
        "pseudocode": """FUNCTION ProcessDarajaCallback(callback_payload: JSON) -> ReconciliationResult:
    INPUT: callback_payload (Body.stkCallback)
    OUTPUT: ReconciliationResult

    stk_data = callback_payload["Body"]["stkCallback"]
    checkout_id = stk_data["CheckoutRequestID"]
    result_code = stk_data["ResultCode"]

    // 1. Idempotency Guard (Prevent double-processing of replayed webhooks)
    IF Redis.Exists("processed_daraja:" + checkout_id) THEN
        RETURN ReconciliationResult(status="ALREADY_PROCESSED")
    END IF

    // 2. Locate Pending Booking / Escrow Record
    booking = Database.Bookings.FindByCheckoutID(checkout_id)
    IF booking IS NULL THEN
        RAISE OrphanedTransactionException("No booking mapped to CheckoutID: " + checkout_id)
    END IF

    // 3. Evaluate Safaricom Result Code
    IF result_code == 0 THEN
        // SUCCESSFUL TRANSACTION
        metadata = ParseCallbackMetadata(stk_data["CallbackMetadata"])
        mpesa_receipt = metadata["MpesaReceiptNumber"] // e.g., 'RJK894KL9'
        amount_paid = metadata["Amount"]

        BEGIN TRANSACTION
            // Post Double-Entry Journal Entry
            ledger_id = DoubleEntryLedgerService.PostTransaction(
                debit_account="ESCROW_TRUST_CASH",
                credit_account="CLIENT_DEPOSIT_LIABILITY",
                amount=amount_paid,
                reference=mpesa_receipt,
                rail="MPESA_DARAJA"
            )

            // Update Booking State
            Database.Bookings.UpdateStatus(booking.id, "CONFIRMED_ESCROW_LOCKED")
            
            // Release Slot Lock (Promoted to permanent booking)
            Redis.Delete("slot_lock:" + booking.consultant_id + ":" + booking.start_time)

            // Mark Webhook Processed in Redis with 72-hour TTL
            Redis.Set("processed_daraja:" + checkout_id, mpesa_receipt, EX=259200)
        COMMIT TRANSACTION

        // Asynchronously notify client & consultant with calendar invite
        CeleryWorker.EnqueueTask("DispatchBookingConfirmationNotice", booking.id)
        
        RETURN ReconciliationResult(status="SUCCESS", receipt=mpesa_receipt)
    ELSE
        // TRANSACTION CANCELLED OR INSUFFICIENT FUNDS
        Database.Bookings.UpdateStatus(booking.id, "PAYMENT_FAILED", Reason=stk_data["ResultDesc"])
        RETURN ReconciliationResult(status="FAILED", error=stk_data["ResultDesc"])
    END IF
END FUNCTION"""
    },
    {
        "id": "PROG-06",
        "name": "MilestoneEscrowLifecycleStateMachine",
        "module_type": "Core Domain Business State Machine",
        "language_framework": "Python 3.12 / SQLAlchemy 2.0 / PostgreSQL Row-Level Locking",
        "description": "Governs the deterministic state transitions of consulting Statement of Work (SOW) milestone escrow contracts: DRAFT -> FUNDED_ACTIVE -> SUBMITTED_UNDER_REVIEW -> (REVISIONS_REQUESTED | IN_DISPUTE) -> APPROVED_RELEASED.",
        "cohesion_type": "Communicational Cohesion (All operations manipulate the same persistent EscrowMilestone entity)",
        "coupling_level": "Data Coupling",
        "fan_in": 4, # Client UI, Consultant UI, Timer Daemon, Dispute Service
        "fan_out": 3, # EscrowLedger, DeliverableStorage, KRAeTIMSService
        "events": [
            "EVT-MILESTONE-SUBMIT: Consultant delivers milestone artifacts.",
            "EVT-MILESTONE-APPROVE: Client authorizes milestone release.",
            "EVT-72HR-AUTO-APPROVE: 72-hour inspection clock expires without dispute."
        ],
        "inputs": [
            ("transition_cmd", "MilestoneTransitionCommandDTO", "milestone_id, actor_id, target_state, auth_payload")
        ],
        "outputs": [
            ("transition_event", "MilestoneTransitionEventDTO", "milestone_id, previous_state, new_state, timestamp")
        ],
        "pseudocode": """FUNCTION TransitionMilestone(milestone_id: UUID, target_state: Enum, actor: UserContext) -> TransitionResult:
    INPUT: milestone_id, target_state, actor
    OUTPUT: TransitionResult (success, previous_state, new_state)

    // Acquire pessimistic row-level lock to prevent concurrent state updates
    milestone = Database.EscrowMilestones.FindWithPessimisticLock(milestone_id)

    // Validate State Transition Matrix
    current_state = milestone.status
    IF NOT IsValidTransition(current_state, target_state) THEN
        RAISE InvalidStateTransitionException("Cannot transition milestone from " + current_state + " to " + target_state)
    END IF

    SWITCH target_state:
        CASE "SUBMITTED_UNDER_REVIEW":
            ASSERT actor.role == "CONSULTANT" AND actor.id == milestone.consultant_id
            milestone.deliverable_sha256 = actor.payload.sha256_hash
            milestone.submitted_at = NOW()
            milestone.inspection_deadline = NOW() + (72 * 3600) // 72 Hours
            
            // Schedule Celery auto-approval task for exactly 72 hours later
            task_id = CeleryScheduler.ScheduleTaskAt(
                "Enforce72HourAutoApproval", 
                run_at=milestone.inspection_deadline, 
                args=[milestone_id]
            )
            milestone.auto_approval_task_id = task_id
            BREAK

        CASE "APPROVED_RELEASED":
            // Can be triggered by Client explicitly or Timer automatically
            ASSERT (actor.role == "CLIENT" AND actor.id == milestone.client_id) OR (actor.is_system_timer == TRUE)
            
            // Cancel pending 72-hour auto-approval worker task if manually approved
            IF milestone.auto_approval_task_id IS NOT NULL THEN
                CeleryScheduler.CancelTask(milestone.auto_approval_task_id)
            END IF

            // Trigger settlement pipeline
            SettlementService.DisburseMilestonePayout(milestone)
            milestone.approved_at = NOW()
            BREAK

        CASE "FROZEN_DISPUTE":
            ASSERT (actor.id == milestone.client_id) OR (actor.id == milestone.consultant_id)
            IF milestone.auto_approval_task_id IS NOT NULL THEN
                CeleryScheduler.CancelTask(milestone.auto_approval_task_id) // Halt clock immediately
            END IF
            milestone.dispute_raised_at = NOW()
            BREAK
    END SWITCH

    milestone.status = target_state
    Database.Save(milestone)

    RETURN TransitionResult(success=TRUE, previous=current_state, new=target_state)
END FUNCTION"""
    },
    {
        "id": "PROG-07",
        "name": "KRAeTIMSTaxAndLedgerSettlementEngine",
        "module_type": "Accounting & Regulatory Compliance Processor",
        "language_framework": "Python 3.12 / HTTPX Resilient Client / KRA Public Key Cryptography",
        "description": "Calculates platform commission take rate (5-8%), generates compliant electronic tax invoices via KRA eTIMS API, embeds verified cryptographic QR codes, posts double-entry financial ledger records, and initiates M-Pesa B2C net payouts to consultants.",
        "cohesion_type": "Sequential Cohesion (Commission calculation -> Tax invoice -> B2C transfer -> Ledger settlement)",
        "coupling_level": "Data Coupling",
        "fan_in": 2, # Milestone Lifecycle Machine, Advisory Booking Service
        "fan_out": 4, # KRA API, M-Pesa B2C Rail, DoubleEntryLedger, PDF Generator
        "events": [
            "EVT-SETTLEMENT-TRIGGER: Approved milestone or completed consultation signals disbursement."
        ],
        "inputs": [
            ("settlement_order", "SettlementOrderDTO", "contract_id, milestone_id, gross_amount_kes, consultant_id, client_id")
        ],
        "outputs": [
            ("settlement_receipt", "SettlementReceiptDTO", "etims_qr_url, b2c_transaction_code, net_payout_kes, platform_fee_kes")
        ],
        "pseudocode": """FUNCTION ExecuteDisbursementAndTaxInvoicing(order: SettlementOrder) -> SettlementReceipt:
    INPUT: order (gross_kes, consultant_id, client_id)
    OUTPUT: SettlementReceipt

    gross_sum = order.gross_amount_kes
    commission_rate = 0.07 // 7% platform take rate
    platform_take = gross_sum * commission_rate
    withholding_tax = gross_sum * 0.05 // 5% statutory Kenyan WHT on professional services
    net_payout = gross_sum - platform_take - withholding_tax

    // 1. Submit Electronic Tax Invoice to Kenya Revenue Authority eTIMS Gateway
    etims_payload = {
        "seller_pin": PlatformConfig.KRA_PIN,
        "buyer_pin": Database.Users.GetTaxPIN(order.client_id),
        "total_amount": gross_sum,
        "taxable_amount": platform_take,
        "tax_amount": platform_take * 0.16 // 16% VAT on platform commission
    }
    
    eTIMS_response = ResilientHTTPClient.PostWithRetry(
        url=PlatformConfig.KRA_ETIMS_ENDPOINT,
        data=etims_payload,
        max_retries=5,
        backoff_factor=1.5
    )
    qr_code_signature = eTIMS_response["qr_code_url"]
    invoice_number = eTIMS_response["invoice_number"]

    // 2. Post Multi-Leg Double-Entry Accounting Records
    BEGIN TRANSACTION
        // Record Commission Income
        DoubleEntryLedgerService.PostTransaction("CLIENT_DEPOSIT_LIABILITY", "PLATFORM_REVENUE", platform_take, invoice_number)
        // Record Withholding Tax Held for KRA Remittance
        DoubleEntryLedgerService.PostTransaction("CLIENT_DEPOSIT_LIABILITY", "KRA_WHT_PAYABLE", withholding_tax, invoice_number)
        // Record Consultant Remuneration
        DoubleEntryLedgerService.PostTransaction("CLIENT_DEPOSIT_LIABILITY", "CONSULTANT_PAYABLE", net_payout, invoice_number)
    COMMIT TRANSACTION

    // 3. Trigger Safaricom M-Pesa B2C Bulk Mobile Payout
    consultant_phone = Database.Users.GetPhone(order.consultant_id)
    b2c_response = SafaricomB2CClient.DisburseSalary(
        phone_number=consultant_phone,
        amount=net_payout,
        remarks="KenyaConsult Payout: " + invoice_number
    )

    // 4. Update Milestone and Consultant Track Record
    Database.ConsultantProfile.IncrementCompletedEscrow(order.consultant_id, amount=gross_sum)
    Database.Milestones.MarkSettled(order.milestone_id, invoice=invoice_number, b2c_ref=b2c_response.ConversationID)

    RETURN SettlementReceipt(
        invoice_no=invoice_number,
        qr_url=qr_code_signature,
        b2c_code=b2c_response.ConversationID,
        net_paid=net_payout
    )
END FUNCTION"""
    },
    {
        "id": "PROG-08",
        "name": "EscrowDisputeAdjudicationEngine",
        "module_type": "Legal & Arbitration Domain Service",
        "language_framework": "Python 3.12 / ReportLab PDF Engine / Cryptography",
        "description": "Aggregates evidence dossiers (SOW clauses, git commits, delivery SHA-256 hashes), coordinates 48-hour counter-party rebuttals, computes prorated apportionment mathematics, and generates legally binding cryptographically signed Adjudication Certificate PDFs.",
        "cohesion_type": "Functional Cohesion (Dedicated arbitration analysis and dispute resolution)",
        "coupling_level": "Data Coupling",
        "fan_in": 2, # Mediator Portal, Client/Consultant Dispute UI
        "fan_out": 3, # EscrowLedger, StorageVault, LegalPDFEngine
        "events": [
            "EVT-DISPUTE-RAISED: Party halts milestone and requests mediation.",
            "EVT-RULING-SIGNED: Mediator signs binding apportionment decision."
        ],
        "inputs": [
            ("dispute_submission", "DisputeSubmissionDTO", "milestone_id, reason_category, evidence_urls, claimant_id"),
            ("mediator_ruling", "MediatorRulingDTO", "case_id, mediator_id, consultant_percent, client_percent, legal_rationale, hardware_sig")
        ],
        "outputs": [
            ("dossier_packet", "DisputeDossierDTO", "case_id, contract_clauses, file_diffs, rebuttal_deadline"),
            ("ruling_certificate", "RulingCertificateDTO", "certificate_pdf_url, disbursement_execution_id, closed_at")
        ],
        "pseudocode": """FUNCTION ExecuteAdjudicationRuling(case_id: UUID, ruling: MediatorRuling) -> RulingCertificate:
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
END FUNCTION"""
    }
]

# Write individual program specification files
for p in programs_data:
    p_path = os.path.join(programs_dir, f"{p['id']}_{p['name']}.md")
    lines = [
        f"# Program Specification: {p['name']}",
        f"**Program ID:** `{p['id']}` | **Module Type:** {p['module_type']}",
        f"**Language / Framework:** `{p['language_framework']}`\n",
        f"### Description\n{p['description']}\n",
        f"### Systems Design Characteristics",
        f"- **Cohesion Type:** {p['cohesion_type']}",
        f"- **Coupling Level:** {p['coupling_level']}",
        f"- **Fan-In:** `{p['fan_in']}` (High reuse by upstream callers)",
        f"- **Fan-Out:** `{p['fan_out']}` (Optimal controlled subordinate delegations)\n",
        f"### Associated Events & Triggers",
        "\n".join([f"- `{evt}`" for evt in p['events']]),
        "\n### Program Input Parameters",
        "| Input Parameter | Data Transfer Object (DTO) | Internal Elements |",
        "| :--- | :--- | :--- |"
    ]
    for inp in p['inputs']:
        lines.append(f"| **`{inp[0]}`** | `{inp[1]}` | {inp[2]} |")
    
    lines.extend([
        "\n### Program Output Returns",
        "| Output Return | Data Transfer Object (DTO) | Internal Elements |",
        "| :--- | :--- | :--- |"
    ])
    for out in p['outputs']:
        lines.append(f"| **`{out[0]}`** | `{out[1]}` | {out[2]} |")
        
    lines.extend([
        "\n### Detailed Algorithmic Pseudocode",
        "```python",
        p['pseudocode'],
        "```\n"
    ])

    with open(p_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# Write Programs Index
with open(os.path.join(programs_dir, "INDEX.md"), "w", encoding="utf-8") as f:
    f.write("# Master Program Specifications Index\n\n")
    f.write("| ID | Program Name | Module Type | Cohesion | Coupling | Fan-In / Out |\n")
    f.write("| :--- | :--- | :--- | :--- | :--- | :---: |\n")
    for p in programs_data:
        f.write(f"| **{p['id']}** | [`{p['name']}`](file:///c:/Users/user/Documents/KenyaConsult/sad_phase3_program_design/programs/{p['id']}_{p['name']}.md) | {p['module_type']} | {p['cohesion_type'].split(' ')[0]} | {p['coupling_level'].split(' ')[0]} | {p['fan_in']} / {p['fan_out']} |\n")

print(f"Generated {len(programs_data)} program specification files in {programs_dir}")
