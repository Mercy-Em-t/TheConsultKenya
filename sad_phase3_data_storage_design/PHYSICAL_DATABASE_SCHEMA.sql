-- ============================================================================
-- Consult Kenya: Physical Database DDL Schema (PostgreSQL 16 + pgvector)
-- Phase 3: Systems Design — Data Storage Specification
-- ============================================================================

-- Enable Required Physical Database Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector"; -- pgvector for 256-dim dense semantic embeddings

-- Define Enumerated Types
CREATE TYPE user_role_enum AS ENUM ('CLIENT', 'CONSULTANT', 'ADMIN', 'MEDIATOR');
CREATE TYPE account_status_enum AS ENUM ('ACTIVE', 'SUSPENDED', 'PENDING_VERIFICATION');
CREATE TYPE authority_tier_enum AS ENUM ('TIER_1_EMERGING', 'TIER_2_ESTABLISHED', 'TIER_3_AUTHORITY');
CREATE TYPE credential_type_enum AS ENUM ('NATIONAL_ID', 'KRA_PIN', 'LSK_ADVOCATE', 'ICPAK_CPA', 'EBK_ENGINEER');
CREATE TYPE verification_status_enum AS ENUM ('PENDING', 'VERIFIED_ACTIVE', 'REJECTED', 'EXPIRED');
CREATE TYPE publication_status_enum AS ENUM ('DRAFT', 'PUBLISHED', 'UNDER_MODERATION', 'REDACTED');
CREATE TYPE proof_type_enum AS ENUM ('GITHUB_COMMIT', 'LIVE_URL', 'CLIENT_COSIGN', 'AUDIT_MEMO_PDF');
CREATE TYPE booking_status_enum AS ENUM ('PENDING_PAYMENT', 'CONFIRMED', 'IN_SESSION', 'COMPLETED', 'CANCELLED', 'NO_SHOW');
CREATE TYPE contract_status_enum AS ENUM ('DRAFT', 'FUNDED_ACTIVE', 'IN_DISPUTE', 'COMPLETED_RELEASED', 'REFUNDED');
CREATE TYPE milestone_status_enum AS ENUM ('PENDING_FUNDING', 'FUNDED_LOCKED', 'SUBMITTED', 'REVISIONS_REQUESTED', 'APPROVED_RELEASED', 'FROZEN_DISPUTE');
CREATE TYPE payment_rail_enum AS ENUM ('MPESA_DARAJA', 'CARD_PAYSTACK', 'RTGS_WIRE', 'MPESA_B2C');

-- ----------------------------------------------------------------------------
-- Table 1: tbl_users (Kernel Independent Entity)
-- ----------------------------------------------------------------------------
CREATE TABLE tbl_users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(150) NOT NULL,
    primary_email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    user_role user_role_enum NOT NULL DEFAULT 'CLIENT',
    password_hash VARCHAR(255) NOT NULL,
    mfa_secret VARCHAR(64),
    account_status account_status_enum NOT NULL DEFAULT 'ACTIVE',
    row_version INTEGER NOT NULL DEFAULT 1, -- Optimistic concurrency lock
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ -- Soft deletion timestamp
);

-- ----------------------------------------------------------------------------
-- Table 2: tbl_consultant_profiles (Subtype Characteristic Entity)
-- ----------------------------------------------------------------------------
CREATE TABLE tbl_consultant_profiles (
    consultant_id UUID PRIMARY KEY REFERENCES tbl_users(user_id) ON DELETE CASCADE,
    public_handle VARCHAR(50) NOT NULL UNIQUE,
    professional_headline VARCHAR(200) NOT NULL,
    cas_score NUMERIC(6,2) NOT NULL DEFAULT 100.00 CHECK (cas_score >= 0 AND cas_score <= 1000),
    authority_tier authority_tier_enum NOT NULL DEFAULT 'TIER_1_EMERGING',
    hourly_rate_kes NUMERIC(10,2) NOT NULL CHECK (hourly_rate_kes >= 2500.00),
    bento_grid_layout JSONB NOT NULL DEFAULT '{}'::jsonb,
    total_escrow_completed INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- Table 3: tbl_professional_credentials (Weak Dependent Entity)
-- ----------------------------------------------------------------------------
CREATE TABLE tbl_professional_credentials (
    credential_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consultant_id UUID NOT NULL REFERENCES tbl_consultant_profiles(consultant_id) ON DELETE CASCADE,
    credential_type credential_type_enum NOT NULL,
    license_number VARCHAR(100) NOT NULL,
    verification_status verification_status_enum NOT NULL DEFAULT 'PENDING',
    registry_response_hash CHAR(64),
    verified_at TIMESTAMPTZ,
    expiry_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- Table 4: tbl_topic_tags (Lookup Taxonomy Entity)
-- ----------------------------------------------------------------------------
CREATE TABLE tbl_topic_tags (
    tag_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tag_name VARCHAR(60) NOT NULL UNIQUE,
    category_domain VARCHAR(60) NOT NULL,
    is_featured BOOLEAN NOT NULL DEFAULT FALSE
);

-- ----------------------------------------------------------------------------
-- Table 5: tbl_case_study_decks (Core Content Entity with pgvector)
-- ----------------------------------------------------------------------------
CREATE TABLE tbl_case_study_decks (
    case_study_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    author_id UUID NOT NULL REFERENCES tbl_consultant_profiles(consultant_id) ON DELETE RESTRICT,
    case_title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    executive_summary TEXT NOT NULL,
    content_blueprint_json JSONB NOT NULL,
    conversion_anchor_json JSONB NOT NULL,
    semantic_embedding vector(256) NOT NULL, -- 256-dimensional dense embedding
    publication_status publication_status_enum NOT NULL DEFAULT 'DRAFT',
    view_count INTEGER NOT NULL DEFAULT 0,
    bookmark_count INTEGER NOT NULL DEFAULT 0,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- Table 6: tbl_execution_proofs (Characteristic Dependent Entity)
-- ----------------------------------------------------------------------------
CREATE TABLE tbl_execution_proofs (
    proof_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_study_id UUID NOT NULL REFERENCES tbl_case_study_decks(case_study_id) ON DELETE CASCADE,
    proof_type proof_type_enum NOT NULL,
    external_uri VARCHAR(500),
    sha256_fingerprint CHAR(64) NOT NULL,
    is_externally_verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- Table 7: tbl_case_study_tags (Intersection Entity M:N)
-- ----------------------------------------------------------------------------
CREATE TABLE tbl_case_study_tags (
    case_study_id UUID NOT NULL REFERENCES tbl_case_study_decks(case_study_id) ON DELETE CASCADE,
    tag_id UUID NOT NULL REFERENCES tbl_topic_tags(tag_id) ON DELETE CASCADE,
    relevance_score NUMERIC(4,3) NOT NULL DEFAULT 1.000,
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (case_study_id, tag_id)
);

-- ----------------------------------------------------------------------------
-- Table 8: tbl_user_bookmarks (Intersection Entity M:N)
-- ----------------------------------------------------------------------------
CREATE TABLE tbl_user_bookmarks (
    user_id UUID NOT NULL REFERENCES tbl_users(user_id) ON DELETE CASCADE,
    case_study_id UUID NOT NULL REFERENCES tbl_case_study_decks(case_study_id) ON DELETE CASCADE,
    collection_name VARCHAR(100) NOT NULL DEFAULT 'Default',
    saved_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, case_study_id)
);

-- ----------------------------------------------------------------------------
-- Table 9: tbl_consultation_bookings (Operational Transaction Entity)
-- ----------------------------------------------------------------------------
CREATE TABLE tbl_consultation_bookings (
    booking_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL REFERENCES tbl_users(user_id) ON DELETE RESTRICT,
    consultant_id UUID NOT NULL REFERENCES tbl_consultant_profiles(consultant_id) ON DELETE RESTRICT,
    case_study_anchor_id UUID REFERENCES tbl_case_study_decks(case_study_id) ON DELETE SET NULL,
    scheduled_start_time TIMESTAMPTZ NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 45,
    session_status booking_status_enum NOT NULL DEFAULT 'PENDING_PAYMENT',
    webrtc_room_token VARCHAR(255),
    total_fee_kes NUMERIC(10,2) NOT NULL,
    lock_token UUID, -- Tracks 15-minute Redis slot reservation token
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- Table 10: tbl_escrow_contracts (Contract Aggregate Entity)
-- ----------------------------------------------------------------------------
CREATE TABLE tbl_escrow_contracts (
    contract_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL REFERENCES tbl_users(user_id) ON DELETE RESTRICT,
    consultant_id UUID NOT NULL REFERENCES tbl_consultant_profiles(consultant_id) ON DELETE RESTRICT,
    contract_title VARCHAR(200) NOT NULL,
    contract_status contract_status_enum NOT NULL DEFAULT 'DRAFT',
    total_contract_value_kes NUMERIC(12,2) NOT NULL,
    platform_commission_rate NUMERIC(4,4) NOT NULL DEFAULT 0.0700,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- Table 11: tbl_escrow_milestones (Dependent Tranche Entity)
-- ----------------------------------------------------------------------------
CREATE TABLE tbl_escrow_milestones (
    milestone_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id UUID NOT NULL REFERENCES tbl_escrow_contracts(contract_id) ON DELETE CASCADE,
    sequence_number SMALLINT NOT NULL,
    milestone_title VARCHAR(150) NOT NULL,
    milestone_amount_kes NUMERIC(12,2) NOT NULL,
    milestone_status milestone_status_enum NOT NULL DEFAULT 'PENDING_FUNDING',
    deliverable_sha256 CHAR(64),
    inspection_deadline TIMESTAMPTZ,
    auto_approval_task_id VARCHAR(100),
    approved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_contract_sequence UNIQUE (contract_id, sequence_number)
);

-- ----------------------------------------------------------------------------
-- Table 12: tbl_ledger_transactions (Partitioned Immutable Double-Entry Ledger)
-- Partitioned by RANGE on created_at for high-throughput operational stamina
-- ----------------------------------------------------------------------------
CREATE TABLE tbl_ledger_transactions (
    transaction_id UUID DEFAULT gen_random_uuid(),
    booking_id UUID REFERENCES tbl_consultation_bookings(booking_id),
    milestone_id UUID REFERENCES tbl_escrow_milestones(milestone_id),
    debit_account VARCHAR(50) NOT NULL,
    credit_account VARCHAR(50) NOT NULL,
    amount_kes NUMERIC(12,2) NOT NULL CHECK (amount_kes > 0),
    payment_rail payment_rail_enum NOT NULL,
    external_reference VARCHAR(100) NOT NULL,
    etims_invoice_number VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (transaction_id, created_at)
) PARTITION BY RANGE (created_at);

-- Create 2026/2027 Initial Partitions
CREATE TABLE tbl_ledger_transactions_2026_h2 PARTITION OF tbl_ledger_transactions
    FOR VALUES FROM ('2026-07-01 00:00:00+00') TO ('2027-01-01 00:00:00+00');
CREATE TABLE tbl_ledger_transactions_2027_h1 PARTITION OF tbl_ledger_transactions
    FOR VALUES FROM ('2027-01-01 00:00:00+00') TO ('2027-07-01 00:00:00+00');

-- ============================================================================
-- Physical Database Indexes (B-Tree, HNSW Vector, Partial, and Inverted GIN)
-- ============================================================================

-- 1. Vector Similarity Index (HNSW Index for Cosine Distance on Case Studies)
CREATE INDEX idx_case_studies_embedding_hnsw 
ON tbl_case_study_decks 
USING hnsw (semantic_embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 2. Discovery Feed Filter Partial Index (Only active published cards)
CREATE INDEX idx_case_studies_published_feed 
ON tbl_case_study_decks (published_at DESC) 
WHERE publication_status = 'PUBLISHED';

-- 3. Composite Foreign Key & Concurrency Indexes
CREATE INDEX idx_bookings_consultant_time 
ON tbl_consultation_bookings (consultant_id, scheduled_start_time);

CREATE INDEX idx_bookings_status 
ON tbl_consultation_bookings (session_status);

CREATE INDEX idx_milestones_contract_status 
ON tbl_escrow_milestones (contract_id, milestone_status);

-- 4. Unique Reference Index on Ledger for Idempotency
CREATE INDEX idx_ledger_external_reference 
ON tbl_ledger_transactions (external_reference);

-- 5. Inverted GIN Indexes for JSONB Bento Grids and Blueprint Queries
CREATE INDEX idx_bento_grid_gin 
ON tbl_consultant_profiles USING gin (bento_grid_layout);

CREATE INDEX idx_content_blueprint_gin 
ON tbl_case_study_decks USING gin (content_blueprint_json);

-- ============================================================================
-- Physical Table Clustering
-- ============================================================================
-- Physically order tbl_case_study_decks on disk by published_at index to accelerate range scans
CLUSTER tbl_case_study_decks USING idx_case_studies_published_feed;
