"""
PROG-06: MilestoneEscrowLifecycleStateMachine
Governs deterministic state transitions of consulting Statement of Work (SOW) milestone escrow contracts:
PENDING_FUNDING -> FUNDED_LOCKED -> SUBMITTED -> (REVISIONS_REQUESTED | FROZEN_DISPUTE) -> APPROVED_RELEASED.
Enforces pessimistic row-level locking and 72-hour automated client inspection clock.
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
    EscrowContract,
    EscrowMilestone,
    User,
    ConsultantProfile
)

router = APIRouter(prefix="/escrow", tags=["PROG-06: Escrow State Machine"])


# -----------------------------------------------------------------------------
# DTO Definitions
# -----------------------------------------------------------------------------

class CreateContractDTO(BaseModel):
    client_id: str
    consultant_id: str
    contract_title: str
    total_contract_value_kes: float = Field(..., gt=0)
    platform_commission_rate: float = Field(default=0.07, ge=0.03, le=0.15)


class CreateMilestoneDTO(BaseModel):
    contract_id: str
    sequence_number: int = Field(..., ge=1)
    milestone_title: str
    milestone_amount_kes: float = Field(..., gt=0)


class MilestoneTransitionCommandDTO(BaseModel):
    milestone_id: str
    actor_id: str
    actor_role: str = Field(..., description="CLIENT, CONSULTANT, MEDIATOR, SYSTEM_TIMER, ADMIN")
    target_state: str = Field(
        ...,
        description="FUNDED_LOCKED, SUBMITTED, REVISIONS_REQUESTED, APPROVED_RELEASED, FROZEN_DISPUTE, CLOSED_DISPUTE_RESOLVED"
    )
    deliverable_sha256: Optional[str] = None
    deliverable_uri: Optional[str] = None
    rejection_reason: Optional[str] = None


class MilestoneTransitionEventDTO(BaseModel):
    milestone_id: str
    contract_id: str
    previous_state: str
    new_state: str
    transitioned_at: datetime.datetime
    inspection_deadline: Optional[datetime.datetime] = None
    is_settled: bool = False
    message: str


# -----------------------------------------------------------------------------
# Valid Transition Matrix
# -----------------------------------------------------------------------------

VALID_TRANSITIONS: Dict[str, List[str]] = {
    "PENDING_FUNDING": ["FUNDED_LOCKED"],
    "FUNDED_LOCKED": ["SUBMITTED", "FROZEN_DISPUTE"],
    "SUBMITTED": ["APPROVED_RELEASED", "REVISIONS_REQUESTED", "FROZEN_DISPUTE"],
    "REVISIONS_REQUESTED": ["SUBMITTED", "FROZEN_DISPUTE"],
    "FROZEN_DISPUTE": ["CLOSED_DISPUTE_RESOLVED"],
    "APPROVED_RELEASED": [],
    "CLOSED_DISPUTE_RESOLVED": []
}


def is_valid_transition(current_state: str, target_state: str) -> bool:
    """Verifies that target_state is an allowable forward transition from current_state."""
    allowed = VALID_TRANSITIONS.get(current_state, [])
    return target_state in allowed


# -----------------------------------------------------------------------------
# Core State Machine Engine
# -----------------------------------------------------------------------------

def transition_milestone(
    cmd: MilestoneTransitionCommandDTO,
    db: Session
) -> MilestoneTransitionEventDTO:
    """
    Executes deterministic state transitions on milestone escrow.
    Acquires row-level pessimistic lock, enforces state machine invariants,
    and coordinates 72-hour auto-approval timers.
    """
    query = db.query(EscrowMilestone).filter(EscrowMilestone.milestone_id == cmd.milestone_id)
    # Pessimistic locking when dialect supports it
    try:
        milestone = query.with_for_update().first()
    except Exception:
        milestone = query.first()

    if not milestone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Milestone {cmd.milestone_id} not found"
        )

    contract = milestone.contract
    current_state = milestone.milestone_status
    target_state = cmd.target_state

    # 1. State Matrix Validation
    if not is_valid_transition(current_state, target_state):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid state transition from '{current_state}' to '{target_state}'. Allowed: {VALID_TRANSITIONS.get(current_state, [])}"
        )

    now = datetime.datetime.utcnow()
    inspection_deadline = milestone.inspection_deadline
    is_settled = False

    # 2. State-Specific Business Invariant Checks
    if target_state == "FUNDED_LOCKED":
        # Funding escrow lock
        contract.contract_status = "FUNDED_ACTIVE"

    elif target_state == "SUBMITTED":
        # Consultant delivering deliverable artifacts
        if cmd.actor_role not in ("CONSULTANT", "ADMIN"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the assigned consultant can submit milestone deliverables."
            )
        if cmd.actor_id != contract.consultant_id and cmd.actor_role != "ADMIN":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Actor ID does not match contract consultant ID."
            )
        if not cmd.deliverable_sha256:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Deliverable SHA-256 fingerprint digest is mandatory."
            )

        milestone.deliverable_sha256 = cmd.deliverable_sha256
        milestone.deliverable_uri = cmd.deliverable_uri
        milestone.submitted_at = now
        # 72-Hour Inspection Clock
        inspection_deadline = now + datetime.timedelta(hours=settings.AUTO_APPROVAL_WINDOW_HOURS)
        milestone.inspection_deadline = inspection_deadline
        # Synthetic Celery task ID
        milestone.auto_approval_task_id = f"auto_approve_{milestone.milestone_id}_{int(now.timestamp())}"

    elif target_state == "APPROVED_RELEASED":
        # Can be triggered by Client or System Timer upon expiry of 72 hours
        is_client = (cmd.actor_role == "CLIENT" and cmd.actor_id == contract.client_id)
        is_timer = (cmd.actor_role == "SYSTEM_TIMER")
        is_admin = (cmd.actor_role == "ADMIN")

        if not (is_client or is_timer or is_admin):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the contracting client or system inspection timer can approve milestone release."
            )

        # Cancel auto-approval timer if manually approved
        milestone.auto_approval_task_id = None
        milestone.approved_at = now
        is_settled = True

        # Check if all milestones are approved to complete whole contract
        all_milestones = db.query(EscrowMilestone).filter(
            EscrowMilestone.contract_id == contract.contract_id,
            EscrowMilestone.milestone_id != milestone.milestone_id
        ).all()
        if all(m.milestone_status == "APPROVED_RELEASED" for m in all_milestones):
            contract.contract_status = "COMPLETED_RELEASED"

    elif target_state == "REVISIONS_REQUESTED":
        # Client requests revisions
        if cmd.actor_role not in ("CLIENT", "ADMIN") or (cmd.actor_role == "CLIENT" and cmd.actor_id != contract.client_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the client can request milestone deliverable revisions."
            )
        # Cancel auto-approval clock
        milestone.auto_approval_task_id = None
        milestone.inspection_deadline = None

    elif target_state == "FROZEN_DISPUTE":
        # Disputed by client or consultant
        if cmd.actor_id not in (contract.client_id, contract.consultant_id) and cmd.actor_role != "ADMIN":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only parties to the contract can initiate an escrow dispute."
            )
        # Halt auto-approval clock immediately
        milestone.auto_approval_task_id = None
        milestone.dispute_raised_at = now
        contract.contract_status = "IN_DISPUTE"

    elif target_state == "CLOSED_DISPUTE_RESOLVED":
        if cmd.actor_role not in ("MEDIATOR", "ADMIN"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only accredited mediators or administrators can close disputed milestones."
            )
        is_settled = True

    # Commit transition
    milestone.milestone_status = target_state
    db.commit()
    db.refresh(milestone)

    return MilestoneTransitionEventDTO(
        milestone_id=milestone.milestone_id,
        contract_id=milestone.contract_id,
        previous_state=current_state,
        new_state=target_state,
        transitioned_at=now,
        inspection_deadline=inspection_deadline,
        is_settled=is_settled,
        message=f"Milestone state successfully transitioned to {target_state}."
    )


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------

@router.post("/contracts")
def create_contract(
    payload: CreateContractDTO,
    db: Session = Depends(get_db)
):
    """Creates a new consulting Statement of Work (SOW) escrow contract draft."""
    contract = EscrowContract(
        client_id=payload.client_id,
        consultant_id=payload.consultant_id,
        contract_title=payload.contract_title,
        total_contract_value_kes=payload.total_contract_value_kes,
        platform_commission_rate=payload.platform_commission_rate,
        contract_status="DRAFT"
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return {
        "contract_id": contract.contract_id,
        "title": contract.contract_title,
        "status": contract.contract_status,
        "total_value_kes": float(contract.total_contract_value_kes)
    }


@router.post("/milestones")
def create_milestone(
    payload: CreateMilestoneDTO,
    db: Session = Depends(get_db)
):
    """Creates a milestone tranche within an escrow contract."""
    contract = db.query(EscrowContract).filter(EscrowContract.contract_id == payload.contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    milestone = EscrowMilestone(
        contract_id=payload.contract_id,
        sequence_number=payload.sequence_number,
        milestone_title=payload.milestone_title,
        milestone_amount_kes=payload.milestone_amount_kes,
        milestone_status="PENDING_FUNDING"
    )
    db.add(milestone)
    db.commit()
    db.refresh(milestone)
    return {
        "milestone_id": milestone.milestone_id,
        "sequence": milestone.sequence_number,
        "title": milestone.milestone_title,
        "amount_kes": float(milestone.milestone_amount_kes),
        "status": milestone.milestone_status
    }


@router.post("/milestones/transition", response_model=MilestoneTransitionEventDTO)
def transition_milestone_endpoint(
    cmd: MilestoneTransitionCommandDTO,
    db: Session = Depends(get_db)
):
    """Executes deterministic state transition on an escrow milestone."""
    return transition_milestone(cmd, db)


@router.get("/milestones/{milestone_id}")
def get_milestone_endpoint(
    milestone_id: str,
    db: Session = Depends(get_db)
):
    """Retrieves current milestone status, inspection clock, and deliverable hash."""
    milestone = db.query(EscrowMilestone).filter(EscrowMilestone.milestone_id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")

    return {
        "milestone_id": milestone.milestone_id,
        "contract_id": milestone.contract_id,
        "sequence": milestone.sequence_number,
        "title": milestone.milestone_title,
        "amount_kes": float(milestone.milestone_amount_kes),
        "status": milestone.milestone_status,
        "deliverable_sha256": milestone.deliverable_sha256,
        "deliverable_uri": milestone.deliverable_uri,
        "inspection_deadline": milestone.inspection_deadline,
        "auto_approval_task_id": milestone.auto_approval_task_id,
        "submitted_at": milestone.submitted_at,
        "approved_at": milestone.approved_at
    }
