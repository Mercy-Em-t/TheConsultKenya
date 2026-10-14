"""
Comprehensive Unit & Integration Test Suite for Consult Kenya Backend Modules (PROG-01 to PROG-08).
Executes live algorithmic, database, and state machine validations.
"""

import os
import uuid
import datetime
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set test environment
os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = "sqlite:///./test_kenyaconsult.db"

from src.app.core.config import settings
from src.app.core.database import (
    Base,
    User,
    ConsultantProfile,
    ProfessionalCredential,
    CaseStudyDeck,
    ConsultationBooking,
    EscrowContract,
    EscrowMilestone,
    LedgerTransaction,
    DisputeCase,
    get_db,
    get_redis_client
)
from src.app.main import app

# Import Core Module Functions & DTOs
from src.app.modules.prog01_auth_verification import (
    hash_password,
    verify_password,
    generate_totp_code,
    verify_totp_code,
    create_jwt_token,
    decode_jwt_token,
    verify_credential,
    normalize_name,
    CredentialSubmissionDTO
)
from src.app.modules.prog02_studio_parser import (
    sanitize_html,
    parse_and_render_mermaid,
    compile_case_study_deck,
    parse_video_media,
    chunk_transcript,
    extract_advisory_metadata,
    RawDraftDTO,
    MediaUploadDTO
)
from src.app.modules.prog03_vector_engine import (
    generate_text_embedding_256,
    cosine_similarity,
    execute_two_pass_recommendation,
    ClientSessionContextDTO
)
from src.app.modules.prog04_slot_lock_manager import (
    acquire_advisory_slot_lock,
    release_advisory_slot_lock,
    check_database_conflict,
    SlotLockRequestDTO,
    SlotReleaseRequestDTO
)
from src.app.modules.prog05_mpesa_daraja import (
    format_phone_number,
    generate_daraja_password,
    initiate_stk_push,
    process_daraja_callback,
    PaymentInitDTO
)
from src.app.modules.prog06_escrow_state_machine import (
    transition_milestone,
    MilestoneTransitionCommandDTO
)
from src.app.modules.prog07_kra_etims_payout import (
    execute_disbursement_and_tax_invoicing,
    SettlementOrderDTO
)
from src.app.modules.prog08_dispute_adjudication import (
    open_escrow_dispute,
    execute_mediator_ruling,
    DisputeSubmissionDTO,
    MediatorRulingDTO
)


# Test Database Setup
TEST_DB_URL = "sqlite:///./test_kenyaconsult.db"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Initializes schema before tests and cleans up afterwards."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    if os.path.exists("./test_kenyaconsult.db"):
        try:
            os.remove("./test_kenyaconsult.db")
        except Exception:
            pass


@pytest.fixture
def db_session():
    """Provides a fresh isolated database session."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def test_client(db_session):
    """FastAPI TestClient with overridden database dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# =============================================================================
# PROG-01 Tests: Auth & Credential Verification
# =============================================================================

def test_prog01_password_hashing_and_jwt():
    pwd = "StrongSecurePassword2026!"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False

    # JWT
    claims = {"sub": "user_123", "role": "CONSULTANT"}
    token = create_jwt_token(claims, 900)
    decoded = decode_jwt_token(token)
    assert decoded["sub"] == "user_123"
    assert decoded["role"] == "CONSULTANT"


def test_prog01_totp_mfa():
    secret = "JBSWY3DPEHPK3PXP"
    code = generate_totp_code(secret)
    assert len(code) == 6
    assert verify_totp_code(secret, code) is True


def test_prog01_statutory_credential_verification(db_session):
    # Setup consultant
    user = User(
        user_id="consultant_alice",
        full_name="Alice Wanjiku",
        primary_email="alice.wanjiku@kenyaconsult.co.ke",
        phone_number="+254712345678",
        user_role="CONSULTANT",
        password_hash=hash_password("Password123!")
    )
    db_session.add(user)
    db_session.flush()

    profile = ConsultantProfile(
        consultant_id=user.user_id,
        public_handle="alicewanjiku",
        professional_headline="Senior Advocate of the High Court of Kenya",
        hourly_rate_kes=6000.0,
        cas_score=150.0,
        authority_tier="TIER_1_EMERGING"
    )
    db_session.add(profile)
    db_session.commit()

    # Submit valid LSK license
    submission = CredentialSubmissionDTO(
        consultant_id="consultant_alice",
        credential_type="LSK_ADVOCATE",
        license_number="LSK/1234/20"
    )

    result = verify_credential(submission, current_user=user, db=db_session)
    assert result.status == "VERIFIED_ACTIVE"
    assert result.new_tier == "TIER_3_AUTHORITY"
    assert result.registry_hash is not None

    # Check updated profile
    db_session.refresh(profile)
    assert profile.authority_tier == "TIER_3_AUTHORITY"
    assert profile.cas_score >= 200.0


# =============================================================================
# PROG-02 Tests: Studio Markdown & Video Parser
# =============================================================================

def test_prog02_markdown_and_mermaid_ast():
    sample_markdown = """
# Scaling Mobile Money in Kenya
This is a comprehensive study of M-Pesa integration.
<script>alert('malicious_xss')</script>
```mermaid
flowchart TD
    Client[Client App] --> Daraja[Safaricom Daraja API]
    Daraja --> Escrow[Escrow Ledger]
```
**Conclusion:** Always verify callback signatures.
"""
    draft = RawDraftDTO(markdown_content=sample_markdown)
    compiled = compile_case_study_deck(draft)

    # Malicious script stripped
    assert "<script>" not in compiled.sanitized_html
    assert "alert(" not in compiled.sanitized_html

    # Diagram compiled to SVG
    assert len(compiled.diagrams) == 1
    assert compiled.diagrams[0].is_valid is True
    assert "<svg" in compiled.diagrams[0].svg
    assert "flowchart" in compiled.diagrams[0].diagram_type.lower()
    assert compiled.word_count > 10
    assert compiled.read_time_seconds > 0.0


def test_prog02_video_and_transcript_chunking():
    # Video metadata
    upload = MediaUploadDTO(
        file_name="advisory_session_01.mp4",
        mime_type="video/mp4",
        file_size_bytes=45_000_000,
        media_url="https://s3.af-south-1.amazonaws.com/videos/advisory_01.mp4",
        duration_seconds=2700.0
    )
    video_meta = parse_video_media(upload)
    assert video_meta.codec == "h264"
    assert video_meta.resolution == "1920x1080"
    assert video_meta.is_playable is True

    # Transcript chunking
    transcript_text = """
[00:00:15] Consultant: Welcome to the KenyaConsult advisory session on KRA eTIMS.
[00:00:45] Client: We need to understand the 5% withholding tax mechanics.
[00:01:30] Consultant: Action item: Configure eTIMS middleware with the KRA PIN.
"""
    chunks = chunk_transcript(transcript_text, window_seconds=60.0)
    assert len(chunks) == 3
    assert chunks[0].speaker == "CONSULTANT"
    assert chunks[1].speaker == "CLIENT"

    # Metadata extraction
    metadata = extract_advisory_metadata("sess_101", transcript_text)
    assert "TAX_COMPLIANCE" in metadata.extracted_topics
    assert len(metadata.action_items) > 0


# =============================================================================
# PROG-03 Tests: Two-Pass Vector Engine & CAS Ranking
# =============================================================================

def test_prog03_vector_embedding_and_two_pass(db_session):
    # Vector generation
    v1 = generate_text_embedding_256("Fintech M-Pesa Daraja Payment API Kenya")
    v2 = generate_text_embedding_256("Fintech M-Pesa Daraja Payment API Kenya")
    v3 = generate_text_embedding_256("Agricultural irrigation and coffee farming in Nyeri")

    assert len(v1) == 256
    assert abs(cosine_similarity(v1, v2) - 1.0) < 1e-4
    assert cosine_similarity(v1, v3) < 0.80

    # Create published case studies for two-pass recommendation
    deck1 = CaseStudyDeck(
        case_study_id="deck_mpesa_01",
        author_id="consultant_alice",
        case_title="Optimizing Daraja STK Push Reliability",
        slug="optimizing-daraja-stk-push",
        executive_summary="Architecture for zero packet drop in M-Pesa webhooks",
        semantic_embedding=v1,
        publication_status="PUBLISHED",
        target_region="KE",
        published_at=datetime.datetime.utcnow()
    )
    db_session.add(deck1)
    db_session.commit()

    context = ClientSessionContextDTO(
        query_text="M-Pesa payment integration",
        geo_tag="KE",
        limit=10
    )
    feed = execute_two_pass_recommendation(context, db_session)
    assert len(feed.cards) >= 1
    top_card = feed.cards[0]
    assert top_card.case_study_id == "deck_mpesa_01"
    assert top_card.composite_score > 0.0


# =============================================================================
# PROG-04 Tests: Distributed Slot Locking & Calendar Coordination
# =============================================================================

def test_prog04_slot_lock_acquisition_and_concurrency(db_session):
    start_time = datetime.datetime.utcnow() + datetime.timedelta(days=2)

    req1 = SlotLockRequestDTO(
        client_id="client_bob",
        consultant_id="consultant_alice",
        scheduled_start_time=start_time,
        duration_minutes=45
    )

    # 1. Client Bob acquires lock
    res1 = acquire_advisory_slot_lock(req1, db_session)
    assert res1.is_locked is True
    assert res1.lock_token is not None

    # 2. Client Charlie attempts same slot -> Collision rejected
    req2 = SlotLockRequestDTO(
        client_id="client_charlie",
        consultant_id="consultant_alice",
        scheduled_start_time=start_time,
        duration_minutes=45
    )
    res2 = acquire_advisory_slot_lock(req2, db_session)
    assert res2.is_locked is False

    # 3. Client Bob renews lock
    req1.existing_lock_token = res1.lock_token
    res_renew = acquire_advisory_slot_lock(req1, db_session)
    assert res_renew.is_locked is True

    # 4. Client Bob releases lock
    release_req = SlotReleaseRequestDTO(
        consultant_id="consultant_alice",
        scheduled_start_time=start_time,
        lock_token=res1.lock_token
    )
    released = release_advisory_slot_lock(release_req, db_session)
    assert released is True


# =============================================================================
# PROG-05 Tests: M-Pesa Daraja Payment & Callback Coordinator
# =============================================================================

def test_prog05_mpesa_daraja_pipeline(db_session):
    # Setup booking
    booking = ConsultationBooking(
        booking_id="booking_daraja_01",
        client_id="client_bob",
        consultant_id="consultant_alice",
        scheduled_start_time=datetime.datetime.utcnow() + datetime.timedelta(days=3),
        duration_minutes=45,
        total_fee_kes=4500.0,
        session_status="PENDING_PAYMENT"
    )
    db_session.add(booking)
    db_session.commit()

    # 1. Initiate STK Push
    init_dto = PaymentInitDTO(
        booking_id="booking_daraja_01",
        phone_number="0712345678",
        amount_kes=4500.0
    )
    stk_res = initiate_stk_push(init_dto, db_session)
    assert stk_res.ResponseCode == "0"
    checkout_id = stk_res.CheckoutRequestID

    # 2. Simulate Webhook Callback from Safaricom
    callback_payload = {
        "Body": {
            "stkCallback": {
                "MerchantRequestID": stk_res.MerchantRequestID,
                "CheckoutRequestID": checkout_id,
                "ResultCode": 0,
                "ResultDesc": "The service request is processed successfully.",
                "CallbackMetadata": {
                    "Item": [
                        {"Name": "Amount", "Value": 4500.0},
                        {"Name": "MpesaReceiptNumber", "Value": "RJK894KL9X"},
                        {"Name": "PhoneNumber", "Value": 254712345678}
                    ]
                }
            }
        }
    }

    recon_res = process_daraja_callback(callback_payload, db_session)
    assert recon_res.status == "SUCCESS"
    assert recon_res.receipt == "RJK894KL9X"

    # Check booking updated to CONFIRMED_ESCROW_LOCKED
    db_session.refresh(booking)
    assert booking.session_status == "CONFIRMED_ESCROW_LOCKED"

    # 3. Idempotency test (Replayed callback)
    duplicate_res = process_daraja_callback(callback_payload, db_session)
    assert duplicate_res.status == "ALREADY_PROCESSED"


# =============================================================================
# PROG-06 Tests: Escrow State Machine
# =============================================================================

def test_prog06_escrow_milestone_transitions(db_session):
    contract = EscrowContract(
        contract_id="contract_escrow_01",
        client_id="client_bob",
        consultant_id="consultant_alice",
        contract_title="Fintech Security Audit SOW",
        total_contract_value_kes=80000.0,
        contract_status="DRAFT"
    )
    milestone = EscrowMilestone(
        milestone_id="milestone_01",
        contract_id=contract.contract_id,
        sequence_number=1,
        milestone_title="Milestone 1: Penetration Testing",
        milestone_amount_kes=40000.0,
        milestone_status="PENDING_FUNDING"
    )
    db_session.add(contract)
    db_session.add(milestone)
    db_session.commit()

    # 1. Fund milestone: PENDING_FUNDING -> FUNDED_LOCKED
    cmd_fund = MilestoneTransitionCommandDTO(
        milestone_id="milestone_01",
        actor_id="client_bob",
        actor_role="CLIENT",
        target_state="FUNDED_LOCKED"
    )
    res_fund = transition_milestone(cmd_fund, db_session)
    assert res_fund.new_state == "FUNDED_LOCKED"

    # 2. Illegal jump test: Cannot transition directly to APPROVED_RELEASED from FUNDED_LOCKED
    cmd_illegal = MilestoneTransitionCommandDTO(
        milestone_id="milestone_01",
        actor_id="client_bob",
        actor_role="CLIENT",
        target_state="APPROVED_RELEASED"
    )
    with pytest.raises(Exception):
        transition_milestone(cmd_illegal, db_session)

    # 3. Consultant submits deliverable: FUNDED_LOCKED -> SUBMITTED
    cmd_submit = MilestoneTransitionCommandDTO(
        milestone_id="milestone_01",
        actor_id="consultant_alice",
        actor_role="CONSULTANT",
        target_state="SUBMITTED",
        deliverable_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        deliverable_uri="s3://kenyaconsult/deliverables/audit_report.pdf"
    )
    res_submit = transition_milestone(cmd_submit, db_session)
    assert res_submit.new_state == "SUBMITTED"
    assert res_submit.inspection_deadline is not None

    # 4. Client approves release: SUBMITTED -> APPROVED_RELEASED
    cmd_approve = MilestoneTransitionCommandDTO(
        milestone_id="milestone_01",
        actor_id="client_bob",
        actor_role="CLIENT",
        target_state="APPROVED_RELEASED"
    )
    res_approve = transition_milestone(cmd_approve, db_session)
    assert res_approve.new_state == "APPROVED_RELEASED"
    assert res_approve.is_settled is True


# =============================================================================
# PROG-07 Tests: KRA eTIMS Tax & Ledger Settlement
# =============================================================================

def test_prog07_etims_tax_and_ledger_payout(db_session):
    order = SettlementOrderDTO(
        contract_id="contract_escrow_01",
        milestone_id="milestone_01",
        gross_amount_kes=100000.00,
        consultant_id="consultant_alice",
        client_id="client_bob",
        client_kra_pin="P059876543A"
    )

    receipt = execute_disbursement_and_tax_invoicing(order, db_session)

    # Arithmetic checks
    assert receipt.gross_amount_kes == 100000.00
    assert receipt.platform_commission_kes == 7000.00   # 7%
    assert receipt.vat_on_commission_kes == 1120.00     # 16% of 7000
    assert receipt.withholding_tax_kes == 5000.00       # 5% statutory WHT
    assert receipt.net_payout_kes == 88000.00           # 100000 - 7000 - 5000

    # Invoicing and payment references
    assert "KRA-ETIMS" in receipt.invoice_number
    assert "itax.kra.go.ke" in receipt.etims_qr_url
    assert "B2C_" in receipt.b2c_transaction_code

    # Double-entry ledger entries check
    assert len(receipt.ledger_transaction_ids) == 3


# =============================================================================
# PROG-08 Tests: Dispute Adjudication Engine
# =============================================================================

def test_prog08_dispute_arbitration_and_certificate(db_session):
    # Setup disputed milestone
    milestone_disp = EscrowMilestone(
        milestone_id="milestone_dispute_01",
        contract_id="contract_escrow_01",
        sequence_number=2,
        milestone_title="Milestone 2: Deployment",
        milestone_amount_kes=50000.0,
        milestone_status="SUBMITTED",
        deliverable_sha256="abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234"
    )
    db_session.add(milestone_disp)
    db_session.commit()

    # 1. Open Dispute
    disp_sub = DisputeSubmissionDTO(
        milestone_id="milestone_dispute_01",
        claimant_id="client_bob",
        reason_category="SPEC_DEVIATION",
        claim_statement="The delivered microservices do not meet latency SLAs agreed in SOW clause 4."
    )
    case = open_escrow_dispute(disp_sub, db_session)
    assert case.status == "UNDER_ADJUDICATION"
    assert case.rebuttal_deadline is not None

    # Check milestone frozen
    db_session.refresh(milestone_disp)
    assert milestone_disp.milestone_status == "FROZEN_DISPUTE"

    # 2. Apportionment sum invariant check (fails if sum != 100%)
    invalid_ruling = MediatorRulingDTO(
        mediator_id="mediator_judge",
        consultant_split_pct=60.0,
        client_split_pct=50.0,  # Sum = 110%
        legal_rationale="Invalid split test"
    )
    with pytest.raises(Exception):
        execute_mediator_ruling(case.case_id, invalid_ruling, db_session)

    # 3. Valid Ruling: 70% Consultant, 30% Client Refund
    valid_ruling = MediatorRulingDTO(
        mediator_id="mediator_judge",
        consultant_split_pct=70.0,
        client_split_pct=30.0,
        legal_rationale="Consultant delivered 70% of scope; client entitled to 30% restitution."
    )
    cert = execute_mediator_ruling(case.case_id, valid_ruling, db_session)

    assert cert.consultant_awarded_kes == 35000.00  # 70% of 50k
    assert cert.client_refunded_kes == 15000.00      # 30% of 50k
    assert "sealed_cert" in cert.certificate_pdf_url
    assert len(cert.certificate_sha256_seal) == 64

    # Case finalized
    db_session.refresh(milestone_disp)
    assert milestone_disp.milestone_status == "CLOSED_DISPUTE_RESOLVED"


# =============================================================================
# FastAPI Integration Endpoint Tests
# =============================================================================

def test_api_healthcheck_endpoint(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("PASS", "WARN")
    assert "database" in data
    assert "redis_lock_cache" in data


def test_api_root_endpoint(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["modules_implemented"]) == 8
