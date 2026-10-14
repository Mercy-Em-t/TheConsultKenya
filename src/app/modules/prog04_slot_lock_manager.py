"""
PROG-04: CalendarCoordinatorAndSlotLockManager
Enforces distributed slot locking via Redis (15-minute TTL, atomic SETNX),
prevents double-booking race conditions, and coordinates calendar conflict detection.
"""

import uuid
import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.app.core.config import settings
from src.app.core.database import (
    get_db,
    get_redis_client,
    ConsultationBooking,
    ConsultantProfile,
    User
)

router = APIRouter(prefix="/calendar", tags=["PROG-04: Slot Lock & Calendar Coordinator"])


# -----------------------------------------------------------------------------
# DTO Definitions
# -----------------------------------------------------------------------------

class SlotLockRequestDTO(BaseModel):
    client_id: str
    consultant_id: str
    scheduled_start_time: datetime.datetime
    duration_minutes: int = Field(default=45, ge=15, le=180)
    case_study_anchor_id: Optional[str] = None
    existing_lock_token: Optional[str] = None


class SlotLockResponseDTO(BaseModel):
    is_locked: bool
    lock_token: Optional[str] = None
    booking_id: Optional[str] = None
    expires_at: Optional[datetime.datetime] = None
    ttl_seconds_remaining: Optional[int] = None
    message: str


class SlotReleaseRequestDTO(BaseModel):
    consultant_id: str
    scheduled_start_time: datetime.datetime
    lock_token: str


class CalendarConflictCheckDTO(BaseModel):
    consultant_id: str
    scheduled_start_time: datetime.datetime
    duration_minutes: int = 45


# -----------------------------------------------------------------------------
# Slot Lock Manager Implementation
# -----------------------------------------------------------------------------

def build_slot_key(consultant_id: str, start_time: datetime.datetime) -> str:
    """Builds standard canonical Redis key for calendar slot lock."""
    iso_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"slot_lock:{consultant_id}:{iso_time}"


def check_database_conflict(
    consultant_id: str,
    start_time: datetime.datetime,
    duration_minutes: int,
    db: Session
) -> bool:
    """Checks if an already confirmed or in-session booking overlaps with the requested interval."""
    end_time = start_time + datetime.timedelta(minutes=duration_minutes)

    # Active states that block the slot
    blocking_statuses = ("CONFIRMED", "CONFIRMED_ESCROW_LOCKED", "IN_SESSION")

    existing_bookings = db.query(ConsultationBooking).filter(
        ConsultationBooking.consultant_id == consultant_id,
        ConsultationBooking.session_status.in_(blocking_statuses)
    ).all()

    for booking in existing_bookings:
        b_start = booking.scheduled_start_time
        if b_start.tzinfo is not None:
            b_start = b_start.replace(tzinfo=None)
        req_start = start_time.replace(tzinfo=None) if start_time.tzinfo is not None else start_time
        b_end = b_start + datetime.timedelta(minutes=booking.duration_minutes)
        req_end = end_time.replace(tzinfo=None) if end_time.tzinfo is not None else end_time

        # Interval overlap condition: (StartA < EndB) and (EndA > StartB)
        if (req_start < b_end) and (req_end > b_start):
            return True

    return False


def acquire_advisory_slot_lock(
    req: SlotLockRequestDTO,
    db: Session
) -> SlotLockResponseDTO:
    """
    PROG-04 Algorithm:
    1. Checks for calendar conflict in database.
    2. Performs atomic Redis SETNX with 900s TTL.
    3. Persists draft booking in PostgreSQL with lock_token.
    """
    redis_client = get_redis_client()
    lock_key = build_slot_key(req.consultant_id, req.scheduled_start_time)
    ttl = settings.SLOT_LOCK_TTL_SECONDS
    now = datetime.datetime.utcnow()

    # 1. Calendar Conflict Check against confirmed bookings
    if check_database_conflict(req.consultant_id, req.scheduled_start_time, req.duration_minutes, db):
        return SlotLockResponseDTO(
            is_locked=False,
            message="Slot is already permanently booked on consultant's schedule."
        )

    # 2. Check if held by existing token (Renewal)
    if req.existing_lock_token:
        current_val = redis_client.get(lock_key)
        if current_val:
            decoded = current_val.decode("utf-8") if isinstance(current_val, bytes) else str(current_val)
            if decoded == req.existing_lock_token:
                redis_client.expire(lock_key, ttl)
                expires_at = now + datetime.timedelta(seconds=ttl)
                return SlotLockResponseDTO(
                    is_locked=True,
                    lock_token=req.existing_lock_token,
                    expires_at=expires_at,
                    ttl_seconds_remaining=ttl,
                    message="Slot lock successfully extended."
                )

    # 3. Atomic Acquisition
    new_token = str(uuid.uuid4())
    is_acquired = redis_client.set(lock_key, new_token, ex=ttl, nx=True)

    if not is_acquired:
        return SlotLockResponseDTO(
            is_locked=False,
            message="Slot currently reserved by another client. Please select an alternate time."
        )

    # 4. Resolve Consultant Hourly Rate
    consultant = db.query(ConsultantProfile).filter(ConsultantProfile.consultant_id == req.consultant_id).first()
    hourly_rate = float(consultant.hourly_rate_kes) if consultant else 2500.0
    calculated_fee = (hourly_rate / 60.0) * req.duration_minutes

    # 5. Persist Draft Booking in PostgreSQL
    booking = ConsultationBooking(
        client_id=req.client_id,
        consultant_id=req.consultant_id,
        case_study_anchor_id=req.case_study_anchor_id,
        scheduled_start_time=req.scheduled_start_time,
        duration_minutes=req.duration_minutes,
        session_status="PENDING_PAYMENT",
        total_fee_kes=calculated_fee,
        lock_token=new_token
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    expires_at = now + datetime.timedelta(seconds=ttl)

    return SlotLockResponseDTO(
        is_locked=True,
        lock_token=new_token,
        booking_id=booking.booking_id,
        expires_at=expires_at,
        ttl_seconds_remaining=ttl,
        message="Slot locked successfully for 15 minutes. Please proceed to payment."
    )


def release_advisory_slot_lock(
    req: SlotReleaseRequestDTO,
    db: Session
) -> bool:
    """Releases distributed lock atomically if token matches."""
    redis_client = get_redis_client()
    lock_key = build_slot_key(req.consultant_id, req.scheduled_start_time)
    current_val = redis_client.get(lock_key)

    if not current_val:
        return True

    decoded = current_val.decode("utf-8") if isinstance(current_val, bytes) else str(current_val)
    if decoded == req.lock_token:
        redis_client.delete(lock_key)
        # Cancel pending draft booking
        booking = db.query(ConsultationBooking).filter(
            ConsultationBooking.lock_token == req.lock_token,
            ConsultationBooking.session_status == "PENDING_PAYMENT"
        ).first()
        if booking:
            booking.session_status = "CANCELLED"
            db.commit()
        return True

    return False


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------

@router.post("/lock-slot", response_model=SlotLockResponseDTO)
def lock_slot_endpoint(
    payload: SlotLockRequestDTO,
    db: Session = Depends(get_db)
):
    """Acquires a 15-minute distributed slot lock to prevent double bookings."""
    res = acquire_advisory_slot_lock(payload, db)
    if not res.is_locked:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=res.message
        )
    return res


@router.post("/release-slot")
def release_slot_endpoint(
    payload: SlotReleaseRequestDTO,
    db: Session = Depends(get_db)
):
    """Explicitly releases an advisory slot reservation."""
    success = release_advisory_slot_lock(payload, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Provided lock token does not match active reservation."
        )
    return {"status": "RELEASED", "message": "Slot reservation released."}


@router.post("/check-availability")
def check_availability_endpoint(
    payload: CalendarConflictCheckDTO,
    db: Session = Depends(get_db)
):
    """Checks if a calendar time slot is available for booking."""
    redis_client = get_redis_client()
    lock_key = build_slot_key(payload.consultant_id, payload.scheduled_start_time)
    is_temporarily_locked = redis_client.exists(lock_key) == 1
    is_db_conflict = check_database_conflict(
        payload.consultant_id,
        payload.scheduled_start_time,
        payload.duration_minutes,
        db
    )

    available = not is_temporarily_locked and not is_db_conflict
    return {
        "consultant_id": payload.consultant_id,
        "scheduled_start_time": payload.scheduled_start_time,
        "is_available": available,
        "reason": None if available else ("Slot is reserved" if is_temporarily_locked else "Slot has confirmed booking")
    }
