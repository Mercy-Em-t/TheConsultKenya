# Program Specification: MilestoneEscrowLifecycleStateMachine
**Program ID:** `PROG-06` | **Module Type:** Core Domain Business State Machine
**Language / Framework:** `Python 3.12 / SQLAlchemy 2.0 / PostgreSQL Row-Level Locking`

### Description
Governs the deterministic state transitions of consulting Statement of Work (SOW) milestone escrow contracts: DRAFT -> FUNDED_ACTIVE -> SUBMITTED_UNDER_REVIEW -> (REVISIONS_REQUESTED | IN_DISPUTE) -> APPROVED_RELEASED.

### Systems Design Characteristics
- **Cohesion Type:** Communicational Cohesion (All operations manipulate the same persistent EscrowMilestone entity)
- **Coupling Level:** Data Coupling
- **Fan-In:** `4` (High reuse by upstream callers)
- **Fan-Out:** `3` (Optimal controlled subordinate delegations)

### Associated Events & Triggers
- `EVT-MILESTONE-SUBMIT: Consultant delivers milestone artifacts.`
- `EVT-MILESTONE-APPROVE: Client authorizes milestone release.`
- `EVT-72HR-AUTO-APPROVE: 72-hour inspection clock expires without dispute.`

### Program Input Parameters
| Input Parameter | Data Transfer Object (DTO) | Internal Elements |
| :--- | :--- | :--- |
| **`transition_cmd`** | `MilestoneTransitionCommandDTO` | milestone_id, actor_id, target_state, auth_payload |

### Program Output Returns
| Output Return | Data Transfer Object (DTO) | Internal Elements |
| :--- | :--- | :--- |
| **`transition_event`** | `MilestoneTransitionEventDTO` | milestone_id, previous_state, new_state, timestamp |

### Detailed Algorithmic Pseudocode
```python
FUNCTION TransitionMilestone(milestone_id: UUID, target_state: Enum, actor: UserContext) -> TransitionResult:
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
END FUNCTION
```
