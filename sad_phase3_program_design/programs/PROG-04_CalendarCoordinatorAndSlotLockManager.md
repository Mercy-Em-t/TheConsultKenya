# Program Specification: CalendarCoordinatorAndSlotLockManager
**Program ID:** `PROG-04` | **Module Type:** Concurrency & Coordination Service
**Language / Framework:** `Python 3.12 / Redis 7.2 Distributed Locks`

### Description
Coordinates real-time calendar availability synchronization across external providers (Google/Outlook) and enforces high-precision 15-minute temporary soft locks on advisory slots to prevent double-booking race conditions.

### Systems Design Characteristics
- **Cohesion Type:** Functional Cohesion (Atomic lock acquisition, renewal, and release)
- **Coupling Level:** Data Coupling
- **Fan-In:** `3` (High reuse by upstream callers)
- **Fan-Out:** `2` (Optimal controlled subordinate delegations)

### Associated Events & Triggers
- `EVT-SLOT-TAP: Client taps calendar time slot.`
- `EVT-LOCK-EXPIRE: 900 seconds elapse without confirmed payment.`

### Program Input Parameters
| Input Parameter | Data Transfer Object (DTO) | Internal Elements |
| :--- | :--- | :--- |
| **`slot_request`** | `SlotLockRequestDTO` | client_id, consultant_id, slot_timestamp, duration_mins |

### Program Output Returns
| Output Return | Data Transfer Object (DTO) | Internal Elements |
| :--- | :--- | :--- |
| **`lock_result`** | `SlotLockResponseDTO` | is_locked, lock_token, expires_at_timestamp |

### Detailed Algorithmic Pseudocode
```python
FUNCTION AcquireAdvisorySlotLock(client_id: UUID, consultant_id: UUID, start_time: Timestamp) -> LockResult:
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
END FUNCTION
```
