"""
Configuration management module for Consult Kenya backend.
Reads configuration from environment variables with sensible production and local fallbacks.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load local .env if present
load_dotenv()


class AppSettings(BaseModel):
    """System-wide application settings."""

    # Application Metadata
    PROJECT_NAME: str = "Consult Kenya Backend API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    DEBUG: bool = Field(default_factory=lambda: os.getenv("DEBUG", "true").lower() in ("true", "1"))
    API_V1_PREFIX: str = "/api/v1"

    # Database Configuration (PostgreSQL 16 + pgvector)
    DATABASE_URL: str = Field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL",
            "sqlite:///./kenyaconsult.db" if os.getenv("ENVIRONMENT") == "test" else
            (os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/kenyaconsult"))
        )
    )
    DB_POOL_SIZE: int = Field(default_factory=lambda: int(os.getenv("DB_POOL_SIZE", "20")))
    DB_MAX_OVERFLOW: int = Field(default_factory=lambda: int(os.getenv("DB_MAX_OVERFLOW", "10")))

    # Redis Concurrency & Distributed Lock Cache
    REDIS_URL: str = Field(
        default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379/0")
    )
    SLOT_LOCK_TTL_SECONDS: int = 900  # 15 minutes strict reservation lock

    # Authentication & JWT Security
    JWT_SECRET_KEY: str = Field(
        default_factory=lambda: os.getenv("JWT_SECRET_KEY", "super-secret-production-signing-key-consult-kenya-2026")
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Safaricom Daraja M-Pesa Rails
    DARAJA_ENVIRONMENT: str = Field(default_factory=lambda: os.getenv("DARAJA_ENVIRONMENT", "sandbox"))
    DARAJA_CONSUMER_KEY: str = Field(default_factory=lambda: os.getenv("DARAJA_CONSUMER_KEY", "test_consumer_key"))
    DARAJA_CONSUMER_SECRET: str = Field(default_factory=lambda: os.getenv("DARAJA_CONSUMER_SECRET", "test_consumer_secret"))
    DARAJA_SHORTCODE: str = Field(default_factory=lambda: os.getenv("DARAJA_SHORTCODE", "174379"))
    DARAJA_PASSKEY: str = Field(
        default_factory=lambda: os.getenv(
            "DARAJA_PASSKEY",
            "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        )
    )
    DARAJA_CALLBACK_URL: str = Field(
        default_factory=lambda: os.getenv(
            "DARAJA_CALLBACK_URL",
            "https://api.kenyaconsult.co.ke/webhooks/daraja/callback"
        )
    )
    DARAJA_B2C_SHORTCODE: str = Field(default_factory=lambda: os.getenv("DARAJA_B2C_SHORTCODE", "600000"))
    DARAJA_B2C_INITIATOR_NAME: str = Field(default_factory=lambda: os.getenv("DARAJA_B2C_INITIATOR_NAME", "apiop45"))
    DARAJA_B2C_SECURITY_CREDENTIAL: str = Field(default_factory=lambda: os.getenv("DARAJA_B2C_SECURITY_CREDENTIAL", "cred_stub"))

    # Kenya Revenue Authority (KRA) eTIMS Compliance
    PLATFORM_KRA_PIN: str = Field(default_factory=lambda: os.getenv("PLATFORM_KRA_PIN", "P051234567Z"))
    KRA_ETIMS_ENDPOINT: str = Field(
        default_factory=lambda: os.getenv("KRA_ETIMS_ENDPOINT", "https://etims.kra.go.ke/api/v1/invoices/sign")
    )
    KRA_ETIMS_BEARER_TOKEN: str = Field(default_factory=lambda: os.getenv("KRA_ETIMS_BEARER_TOKEN", "etims_sandbox_token"))
    PLATFORM_COMMISSION_RATE: float = 0.07  # 7.0% default take-rate
    KENYA_WHT_RATE: float = 0.05            # 5.0% statutory Withholding Tax on professional services
    KENYA_VAT_RATE: float = 0.16            # 16.0% VAT on platform revenue

    # WebRTC / Live Consultation Audio-Video
    LIVEKIT_URL: str = Field(default_factory=lambda: os.getenv("LIVEKIT_URL", "wss://livekit.kenyaconsult.co.ke"))
    LIVEKIT_API_KEY: str = Field(default_factory=lambda: os.getenv("LIVEKIT_API_KEY", "devkey"))
    LIVEKIT_API_SECRET: str = Field(default_factory=lambda: os.getenv("LIVEKIT_API_SECRET", "secretkey"))

    # Escrow State Machine Controls
    AUTO_APPROVAL_WINDOW_HOURS: int = 72    # 72-Hour Inspection clock
    DISPUTE_REBUTTAL_WINDOW_HOURS: int = 48  # 48-Hour Evidence rebuttal clock

    # AWS S3 Storage Vaults
    S3_BUCKET_ARTIFACTS: str = Field(default_factory=lambda: os.getenv("S3_BUCKET_ARTIFACTS", "kenyaconsult-artifacts-vault"))
    S3_BUCKET_DISPUTES: str = Field(default_factory=lambda: os.getenv("S3_BUCKET_DISPUTES", "kenyaconsult-legal-audit-vault"))
    AWS_REGION: str = Field(default_factory=lambda: os.getenv("AWS_REGION", "af-south-1"))


settings = AppSettings()
