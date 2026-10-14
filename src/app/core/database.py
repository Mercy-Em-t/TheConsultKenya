"""
Database connection, session lifecycle, Redis integration, and SQLAlchemy ORM models.
Directly models the Physical Database Schema specified in Phase 3.
"""

import uuid
import datetime
import json
from typing import Generator, Any, Optional, Dict
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Numeric,
    Boolean,
    DateTime,
    Date,
    ForeignKey,
    Text,
    Enum as SAEnum,
    SmallInteger,
    PrimaryKeyConstraint,
    UniqueConstraint,
    CheckConstraint,
    TypeDecorator
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
import redis

from src.app.core.config import settings

# Base Declarative Model
Base = declarative_base()


# Custom Vector Type Fallback (pgvector or raw list)
class VectorType(TypeDecorator):
    """
    Handles pgvector vector(dim) when on PostgreSQL, or serialized JSON list when on other dialects.
    """
    impl = Text
    cache_ok = True

    def __init__(self, dimensions: int = 256, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dimensions = dimensions

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            from sqlalchemy.dialects.postgresql import dialect as pg_dialect
            # Can use native user defined type 'vector'
            from sqlalchemy.types import UserDefinedType
            class NativeVector(UserDefinedType):
                def get_col_spec(self, **kw):
                    return f"vector({self.dimensions})"
            return dialect.type_descriptor(NativeVector())
        return dialect.type_descriptor(Text())

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, list):
            if dialect.name == "postgresql":
                return "[" + ",".join(str(float(x)) for x in value) + "]"
            return json.dumps(value)
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            try:
                # Strip bracket if formatted like '[0.1, 0.2]'
                cleaned = value.strip("[]() ")
                if not cleaned:
                    return []
                return [float(x.strip()) for x in cleaned.split(",")]
            except Exception:
                return []
        return value


# JSON Type fallback for SQLite / PostgreSQL
class JSONType(TypeDecorator):
    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, (dict, list)):
            return json.dumps(value)
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        if isinstance(value, dict):
            return value
        try:
            return json.loads(value)
        except Exception:
            return {}


# -----------------------------------------------------------------------------
# Database Engine Initialization
# -----------------------------------------------------------------------------
db_url = settings.DATABASE_URL
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

connect_args = {}
if "sqlite" in db_url:
    connect_args["check_same_thread"] = False
    engine = create_engine(db_url, connect_args=connect_args)
else:
    engine = create_engine(
        db_url,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_pre_ping=True
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that provides an isolated transactional database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------------------------------------------------
# Redis Client & Resilient In-Memory Fallback
# -----------------------------------------------------------------------------
class InMemoryRedisStub:
    """In-memory key-value store with TTL emulation for offline test execution."""
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._expiry: Dict[str, datetime.datetime] = {}

    def _purge_expired(self, key: str):
        if key in self._expiry and datetime.datetime.utcnow() > self._expiry[key]:
            self._store.pop(key, None)
            self._expiry.pop(key, None)

    def get(self, key: str):
        self._purge_expired(key)
        val = self._store.get(key)
        if isinstance(val, str):
            return val.encode("utf-8")
        return val

    def set(self, key: str, value: Any, ex: Optional[int] = None, nx: bool = False) -> bool:
        self._purge_expired(key)
        if nx and key in self._store:
            return False
        val_str = value.decode("utf-8") if isinstance(value, bytes) else str(value)
        self._store[key] = val_str
        if ex:
            self._expiry[key] = datetime.datetime.utcnow() + datetime.timedelta(seconds=ex)
        return True

    def delete(self, key: str) -> int:
        self._purge_expired(key)
        if key in self._store:
            del self._store[key]
            self._expiry.pop(key, None)
            return 1
        return 0

    def exists(self, key: str) -> int:
        self._purge_expired(key)
        return 1 if key in self._store else 0

    def expire(self, key: str, seconds: int) -> bool:
        self._purge_expired(key)
        if key in self._store:
            self._expiry[key] = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)
            return True
        return False

    def mget(self, *keys):
        result = []
        for k in keys:
            self._purge_expired(k)
            result.append(self._store.get(k))
        return result


_redis_instance = None


def get_redis_client():
    """Returns connected Redis client or in-memory fallback if connection fails."""
    global _redis_instance
    if _redis_instance is not None:
        return _redis_instance
    try:
        client = redis.Redis.from_url(settings.REDIS_URL, socket_timeout=1.0)
        client.ping()
        _redis_instance = client
    except Exception:
        _redis_instance = InMemoryRedisStub()
    return _redis_instance


# -----------------------------------------------------------------------------
# SQLAlchemy Models (tbl_users to tbl_ledger_transactions + tbl_dispute_cases)
# -----------------------------------------------------------------------------

class User(Base):
    """Table 1: tbl_users (Kernel Independent Entity)"""
    __tablename__ = "tbl_users"

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String(150), nullable=False)
    primary_email = Column(String(255), nullable=False, unique=True, index=True)
    phone_number = Column(String(20), nullable=False, unique=True, index=True)
    user_role = Column(
        SAEnum("CLIENT", "CONSULTANT", "ADMIN", "MEDIATOR", name="user_role_enum"),
        nullable=False,
        default="CLIENT"
    )
    password_hash = Column(String(255), nullable=False)
    mfa_secret = Column(String(64), nullable=True)
    account_status = Column(
        SAEnum("ACTIVE", "SUSPENDED", "PENDING_VERIFICATION", name="account_status_enum"),
        nullable=False,
        default="ACTIVE"
    )
    row_version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    consultant_profile = relationship("ConsultantProfile", back_populates="user", uselist=False)
    bookings = relationship("ConsultationBooking", back_populates="client")


class ConsultantProfile(Base):
    """Table 2: tbl_consultant_profiles (Subtype Characteristic Entity)"""
    __tablename__ = "tbl_consultant_profiles"

    consultant_id = Column(String(36), ForeignKey("tbl_users.user_id", ondelete="CASCADE"), primary_key=True)
    public_handle = Column(String(50), nullable=False, unique=True, index=True)
    professional_headline = Column(String(200), nullable=False)
    cas_score = Column(Numeric(6, 2), nullable=False, default=100.00)
    authority_tier = Column(
        SAEnum("TIER_1_EMERGING", "TIER_2_ESTABLISHED", "TIER_3_AUTHORITY", name="authority_tier_enum"),
        nullable=False,
        default="TIER_1_EMERGING"
    )
    hourly_rate_kes = Column(Numeric(10, 2), nullable=False, default=2500.00)
    bento_grid_layout = Column(JSONType, nullable=False, default=dict)
    total_escrow_completed = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="consultant_profile")
    credentials = relationship("ProfessionalCredential", back_populates="consultant")
    case_studies = relationship("CaseStudyDeck", back_populates="author")


class ProfessionalCredential(Base):
    """Table 3: tbl_professional_credentials (Weak Dependent Entity)"""
    __tablename__ = "tbl_professional_credentials"

    credential_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    consultant_id = Column(String(36), ForeignKey("tbl_consultant_profiles.consultant_id", ondelete="CASCADE"), nullable=False)
    credential_type = Column(
        SAEnum("NATIONAL_ID", "KRA_PIN", "LSK_ADVOCATE", "ICPAK_CPA", "EBK_ENGINEER", name="credential_type_enum"),
        nullable=False
    )
    license_number = Column(String(100), nullable=False)
    verification_status = Column(
        SAEnum("PENDING", "VERIFIED_ACTIVE", "REJECTED", "EXPIRED", name="verification_status_enum"),
        nullable=False,
        default="PENDING"
    )
    registry_response_hash = Column(String(64), nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    expiry_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)

    consultant = relationship("ConsultantProfile", back_populates="credentials")


class TopicTag(Base):
    """Table 4: tbl_topic_tags (Lookup Taxonomy Entity)"""
    __tablename__ = "tbl_topic_tags"

    tag_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tag_name = Column(String(60), nullable=False, unique=True)
    category_domain = Column(String(60), nullable=False)
    is_featured = Column(Boolean, nullable=False, default=False)


class CaseStudyDeck(Base):
    """Table 5: tbl_case_study_decks (Core Content Entity with pgvector 256-dim)"""
    __tablename__ = "tbl_case_study_decks"

    case_study_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    author_id = Column(String(36), ForeignKey("tbl_consultant_profiles.consultant_id", ondelete="RESTRICT"), nullable=False)
    case_title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    executive_summary = Column(Text, nullable=False)
    content_blueprint_json = Column(JSONType, nullable=False, default=dict)
    conversion_anchor_json = Column(JSONType, nullable=False, default=dict)
    semantic_embedding = Column(VectorType(256), nullable=False)
    publication_status = Column(
        SAEnum("DRAFT", "PUBLISHED", "UNDER_MODERATION", "REDACTED", name="publication_status_enum"),
        nullable=False,
        default="DRAFT"
    )
    view_count = Column(Integer, nullable=False, default=0)
    bookmark_count = Column(Integer, nullable=False, default=0)
    target_region = Column(String(50), nullable=False, default="KE")
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    author = relationship("ConsultantProfile", back_populates="case_studies")
    proofs = relationship("ExecutionProof", back_populates="case_study")


class ExecutionProof(Base):
    """Table 6: tbl_execution_proofs (Characteristic Dependent Entity)"""
    __tablename__ = "tbl_execution_proofs"

    proof_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    case_study_id = Column(String(36), ForeignKey("tbl_case_study_decks.case_study_id", ondelete="CASCADE"), nullable=False)
    proof_type = Column(
        SAEnum("GITHUB_COMMIT", "LIVE_URL", "CLIENT_COSIGN", "AUDIT_MEMO_PDF", name="proof_type_enum"),
        nullable=False
    )
    external_uri = Column(String(500), nullable=True)
    sha256_fingerprint = Column(String(64), nullable=False)
    is_externally_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)

    case_study = relationship("CaseStudyDeck", back_populates="proofs")


class CaseStudyTag(Base):
    """Table 7: tbl_case_study_tags (Intersection Entity M:N)"""
    __tablename__ = "tbl_case_study_tags"

    case_study_id = Column(String(36), ForeignKey("tbl_case_study_decks.case_study_id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(String(36), ForeignKey("tbl_topic_tags.tag_id", ondelete="CASCADE"), primary_key=True)
    relevance_score = Column(Numeric(4, 3), nullable=False, default=1.000)
    assigned_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)


class UserBookmark(Base):
    """Table 8: tbl_user_bookmarks (Intersection Entity M:N)"""
    __tablename__ = "tbl_user_bookmarks"

    user_id = Column(String(36), ForeignKey("tbl_users.user_id", ondelete="CASCADE"), primary_key=True)
    case_study_id = Column(String(36), ForeignKey("tbl_case_study_decks.case_study_id", ondelete="CASCADE"), primary_key=True)
    collection_name = Column(String(100), nullable=False, default="Default")
    saved_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)


class ConsultationBooking(Base):
    """Table 9: tbl_consultation_bookings (Operational Transaction Entity)"""
    __tablename__ = "tbl_consultation_bookings"

    booking_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String(36), ForeignKey("tbl_users.user_id", ondelete="RESTRICT"), nullable=False)
    consultant_id = Column(String(36), ForeignKey("tbl_consultant_profiles.consultant_id", ondelete="RESTRICT"), nullable=False)
    case_study_anchor_id = Column(String(36), ForeignKey("tbl_case_study_decks.case_study_id", ondelete="SET NULL"), nullable=True)
    scheduled_start_time = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=45)
    session_status = Column(
        SAEnum(
            "PENDING_PAYMENT",
            "CONFIRMED",
            "CONFIRMED_ESCROW_LOCKED",
            "IN_SESSION",
            "COMPLETED",
            "CANCELLED",
            "NO_SHOW",
            "PAYMENT_FAILED",
            name="booking_status_enum"
        ),
        nullable=False,
        default="PENDING_PAYMENT"
    )
    webrtc_room_token = Column(String(255), nullable=True)
    total_fee_kes = Column(Numeric(10, 2), nullable=False)
    lock_token = Column(String(36), nullable=True)
    daraja_checkout_id = Column(String(100), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    client = relationship("User", back_populates="bookings")


class EscrowContract(Base):
    """Table 10: tbl_escrow_contracts (Contract Aggregate Entity)"""
    __tablename__ = "tbl_escrow_contracts"

    contract_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String(36), ForeignKey("tbl_users.user_id", ondelete="RESTRICT"), nullable=False)
    consultant_id = Column(String(36), ForeignKey("tbl_consultant_profiles.consultant_id", ondelete="RESTRICT"), nullable=False)
    contract_title = Column(String(200), nullable=False)
    contract_status = Column(
        SAEnum("DRAFT", "FUNDED_ACTIVE", "IN_DISPUTE", "COMPLETED_RELEASED", "REFUNDED", name="contract_status_enum"),
        nullable=False,
        default="DRAFT"
    )
    total_contract_value_kes = Column(Numeric(12, 2), nullable=False)
    platform_commission_rate = Column(Numeric(4, 4), nullable=False, default=0.0700)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    milestones = relationship("EscrowMilestone", back_populates="contract", cascade="all, delete-orphan")


class EscrowMilestone(Base):
    """Table 11: tbl_escrow_milestones (Dependent Tranche Entity)"""
    __tablename__ = "tbl_escrow_milestones"

    milestone_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    contract_id = Column(String(36), ForeignKey("tbl_escrow_contracts.contract_id", ondelete="CASCADE"), nullable=False)
    sequence_number = Column(SmallInteger, nullable=False)
    milestone_title = Column(String(150), nullable=False)
    milestone_amount_kes = Column(Numeric(12, 2), nullable=False)
    milestone_status = Column(
        SAEnum(
            "PENDING_FUNDING",
            "FUNDED_LOCKED",
            "SUBMITTED",
            "REVISIONS_REQUESTED",
            "APPROVED_RELEASED",
            "FROZEN_DISPUTE",
            "CLOSED_DISPUTE_RESOLVED",
            name="milestone_status_enum"
        ),
        nullable=False,
        default="PENDING_FUNDING"
    )
    deliverable_sha256 = Column(String(64), nullable=True)
    deliverable_uri = Column(String(500), nullable=True)
    inspection_deadline = Column(DateTime(timezone=True), nullable=True)
    auto_approval_task_id = Column(String(100), nullable=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    dispute_raised_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    contract = relationship("EscrowContract", back_populates="milestones")

    __table_args__ = (
        UniqueConstraint("contract_id", "sequence_number", name="uq_contract_sequence"),
    )


class LedgerTransaction(Base):
    """Table 12: tbl_ledger_transactions (Double-Entry Financial Ledger)"""
    __tablename__ = "tbl_ledger_transactions"

    transaction_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    booking_id = Column(String(36), ForeignKey("tbl_consultation_bookings.booking_id"), nullable=True)
    milestone_id = Column(String(36), ForeignKey("tbl_escrow_milestones.milestone_id"), nullable=True)
    debit_account = Column(String(50), nullable=False)
    credit_account = Column(String(50), nullable=False)
    amount_kes = Column(Numeric(12, 2), nullable=False)
    payment_rail = Column(
        SAEnum("MPESA_DARAJA", "CARD_PAYSTACK", "RTGS_WIRE", "MPESA_B2C", name="payment_rail_enum"),
        nullable=False
    )
    external_reference = Column(String(100), nullable=False, index=True)
    etims_invoice_number = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)


class DisputeCase(Base):
    """
    Supplementary Table: tbl_dispute_cases
    Required for PROG-08 dispute adjudication lifecycle (identifies and closes the gap in PHYSICAL_DATABASE_SCHEMA.sql).
    """
    __tablename__ = "tbl_dispute_cases"

    case_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    milestone_id = Column(String(36), ForeignKey("tbl_escrow_milestones.milestone_id"), nullable=False)
    claimant_id = Column(String(36), ForeignKey("tbl_users.user_id"), nullable=False)
    reason_category = Column(String(100), nullable=False)
    status = Column(
        SAEnum("OPEN", "UNDER_ADJUDICATION", "RESOLVED_DISBURSED", "CANCELLED", name="dispute_status_enum"),
        nullable=False,
        default="UNDER_ADJUDICATION"
    )
    rebuttal_deadline = Column(DateTime(timezone=True), nullable=True)
    mediator_id = Column(String(36), ForeignKey("tbl_users.user_id"), nullable=True)
    consultant_split_pct = Column(Numeric(5, 2), nullable=True)
    client_split_pct = Column(Numeric(5, 2), nullable=True)
    legal_rationale = Column(Text, nullable=True)
    certificate_pdf_url = Column(String(500), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


def init_db():
    """Initializes tables in database."""
    Base.metadata.create_all(bind=engine)
