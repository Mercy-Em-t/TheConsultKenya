# Entity Specification: UserAccount
**Entity ID:** `ENT-01` | **Category:** Independent Entity (Kernel Entity)

### Description
Represents an authenticated human user (Client, Consultant, Admin, Mediator) in the KenyaConsult platform. Exists independently without mandatory foreign key parents.

### Attribute Data Dictionary
| Attribute Name | Data Type | Key / Constraint | Functional Description |
| :--- | :--- | :--- | :--- |
| **`user_id`** | `UUID` | PK | Primary unique surrogate key identifier for the user. |
| **`full_name`** | `VARCHAR(150)` | Mandatory | Legal name of the user. |
| **`primary_email`** | `VARCHAR(255)` | Mandatory, Unique | Canonical email address used for identity and notifications. |
| **`phone_number`** | `VARCHAR(20)` | Mandatory, Unique | E.164 formatted telephone number (e.g., +2547XXXXXXXX) for SMS/M-Pesa. |
| **`user_role`** | `ENUM('CLIENT', 'CONSULTANT', 'ADMIN', 'MEDIATOR')` | Mandatory | Primary role controlling platform privileges. |
| **`password_hash`** | `VARCHAR(255)` | Mandatory | Argon2id cryptographic hash of the account password. |
| **`mfa_secret`** | `VARCHAR(64)` | Optional | TOTP multi-factor authentication seed key. |
| **`account_status`** | `ENUM('ACTIVE', 'SUSPENDED', 'PENDING_VERIFICATION')` | Mandatory | Current lifecycle state of the account. |
| **`created_at`** | `TIMESTAMPTZ` | Mandatory | Immutable timestamp when user registered. |

### Relationships & Structural Constraints
| Target Entity | Direction | Cardinality | Modality | Semantic Business Rule |
| :--- | :---: | :---: | :---: | :--- |
| **`ConsultantProfile`** | Parent | `1 : (0,1)` | Optional | A User may optionally have one ConsultantProfile (if role is CONSULTANT). |
| **`CaseStudyDeck`** | Parent | `1 : (0,N)` | Optional | A User (Consultant) may author zero or many CaseStudyDecks. |
| **`ConsultationBooking`** | Parent | `1 : (0,N)` | Optional | A User (Client) may place zero or many ConsultationBookings. |
| **`EscrowContract`** | Parent | `1 : (0,N)` | Optional | A User (Client or Consultant) participates in zero or many EscrowContracts. |
