# Program Specification: AuthAndCredentialVerificationService
**Program ID:** `PROG-01` | **Module Type:** Control & Domain Service
**Language / Framework:** `Python 3.12 / FastAPI / Pydantic v2`

### Description
Authenticates user sessions via Argon2id and TOTP MFA, ingests professional credentials (National ID, KRA PIN, LSK/ICPAK/EBK license #), and executes automated queries against statutory government registry APIs.

### Systems Design Characteristics
- **Cohesion Type:** Functional Cohesion (Executes single, well-defined mathematical and verification tasks)
- **Coupling Level:** Data Coupling (Communicates strictly through typed DTO parameters)
- **Fan-In:** `4` (High reuse by upstream callers)
- **Fan-Out:** `3` (Optimal controlled subordinate delegations)

### Associated Events & Triggers
- `EVT-AUTH-LOGIN: User submits credentials or refresh token.`
- `EVT-AUTH-CRED-SUBMIT: Consultant submits professional license number for verification.`

### Program Input Parameters
| Input Parameter | Data Transfer Object (DTO) | Internal Elements |
| :--- | :--- | :--- |
| **`login_request`** | `LoginDTO` | email, password_hash, otp_code |
| **`credential_payload`** | `CredentialSubmissionDTO` | consultant_id, license_number, board_type, national_id |

### Program Output Returns
| Output Return | Data Transfer Object (DTO) | Internal Elements |
| :--- | :--- | :--- |
| **`auth_token_pair`** | `TokenResponseDTO` | jwt_access_token (15m), refresh_token (7d) |
| **`verification_result`** | `CredentialVerificationResultDTO` | status, verified_at, registry_hash, new_tier |

### Detailed Algorithmic Pseudocode
```python
FUNCTION VerifyProfessionalLicense(consultant_id: UUID, board_type: Enum, license_no: String) -> CredentialResult:
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
END FUNCTION
```
