# Entity Specification: ConsultationBooking
**Entity ID:** `ENT-09` | **Category:** Independent / Operational Transaction Entity

### Description
Represents a scheduled 1-on-1 advisory session between a Client and a Consultant. Manages calendar slots, WebRTC room credentials, and session state.

### Attribute Data Dictionary
| Attribute Name | Data Type | Key / Constraint | Functional Description |
| :--- | :--- | :--- | :--- |
| **`booking_id`** | `UUID` | PK | Primary surrogate key identifier for the booking. |
| **`client_id`** | `UUID` | FK (UserAccount.user_id) | Mandatory client reference. |
| **`consultant_id`** | `UUID` | FK (ConsultantProfile.consultant_id) | Mandatory consultant reference. |
| **`case_study_anchor_id`** | `UUID` | Optional, FK (CaseStudyDeck.case_study_id) | Optional originating case study CTA. |
| **`scheduled_start_time`** | `TIMESTAMPTZ` | Mandatory | Agreed consultation starting timestamp (EAT). |
| **`duration_minutes`** | `INTEGER` | Mandatory, Default: 45 | Length of consultation in minutes. |
| **`session_status`** | `ENUM('PENDING_PAYMENT', 'CONFIRMED', 'IN_SESSION', 'COMPLETED', 'CANCELLED', 'NO_SHOW')` | Mandatory | Lifecycle state. |
| **`webrtc_room_token`** | `VARCHAR(255)` | Optional | Encrypted media room access token. |
| **`total_fee_kes`** | `DECIMAL(10,2)` | Mandatory | Total session fee charged in Kenyan Shillings. |
| **`created_at`** | `TIMESTAMPTZ` | Mandatory | Timestamp when slot reservation was initiated. |

### Relationships & Structural Constraints
| Target Entity | Direction | Cardinality | Modality | Semantic Business Rule |
| :--- | :---: | :---: | :---: | :--- |
| **`UserAccount`** | Child | `(1,1) : 1` | Mandatory | Booked by exactly one Client. |
| **`ConsultantProfile`** | Child | `(1,1) : 1` | Mandatory | Delivered by exactly one Consultant. |
| **`EscrowContract`** | Parent | `1 : (0,1)` | Optional | Tied to zero or one parent EscrowContract. |
| **`LedgerTransaction`** | Parent | `1 : (1,N)` | Mandatory | Has one or many LedgerTransactions. |
