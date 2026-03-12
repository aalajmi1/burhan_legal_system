# DATABASE_SCHEMA.md

## Roles
System roles:
- Admin
- Lawyer
- Client

---

## 1. User
Represents any authenticated system user.

Fields:
- id
- full_name
- email (unique)
- phone
- password
- role (Admin, Lawyer, Client)
- is_active
- created_at
- updated_at
- last_login

Notes:
- Lawyers and Admins are internal users.
- Client can also have a user account for portal access.

---

## 2. Client
Represents a legal client / principal.

Fields:
- id
- full_name
- identity_type
- identity_number
- phone
- email
- address
- iban
- notes
- portal_user_id (nullable, one-to-one with User when client portal is enabled)
- created_at
- updated_at

Identity types:
- NationalID
- Iqama
- CommercialRegistration
- Passport
- Other

---

## 3. PowerOfAttorney
Represents a Najiz authorization / agency record.

Fields:
- id
- client_id
- agency_number
- issue_date
- expiry_date
- status
- notes
- created_at
- updated_at

Status values:
- Active
- Expired
- Revoked
- PendingVerification

Relationship:
- One client can have multiple POA records.

---

## 4. Case
Represents a legal matter.

Fields:
- id
- case_number
- title
- case_type
- court_name
- court_circuit
- status
- priority
- description
- client_id
- assigned_lawyer_id
- power_of_attorney_id (nullable)
- filing_date
- expected_close_date (nullable)
- last_activity_at
- created_at
- updated_at

Case types:
- Commercial
- Civil
- Criminal
- Labor
- Family
- RealEstate
- Enforcement
- Administrative
- Other

Priority values:
- Urgent
- Important
- Normal

---

## 5. CaseAssignmentHistory
Tracks reassignment of a case between lawyers.

Fields:
- id
- case_id
- lawyer_id
- assigned_from
- assigned_to
- assigned_by
- notes

---

## 6. CaseEvent
Represents timeline events for a case.

Fields:
- id
- case_id
- event_type
- title
- description
- event_date
- is_completed
- created_by
- created_at
- updated_at

Event types:
- CourtSession
- AppealDeadline
- ExpertVisit
- ClientMeeting
- InternalReview
- DocumentSubmission
- PaymentDeadline
- JudgmentIssued
- EnforcementAction
- Other

---

## 7. Document
Represents uploaded files.

Fields:
- id
- case_id (nullable)
- client_id (nullable)
- document_type
- title
- file
- file_name
- file_size
- mime_type
- version
- uploaded_by
- is_confidential
- notes
- created_at
- updated_at

Document types:
- PowerOfAttorney
- Judgment
- LegalMemo
- AppealMemo
- Contract
- Evidence
- ExpertReport
- IdentityDocument
- InvoiceAttachment
- Receipt
- CourtNotice
- SessionMinutes
- Other

Rules:
- A document must be linked to at least a case or a client.
- Version starts from 1.

---

## 8. Invoice
Represents a financial invoice.

Fields:
- id
- case_id
- client_id
- invoice_number
- issue_date
- due_date
- fees_amount
- government_fees_amount
- court_costs_amount
- tax_amount
- total_amount
- status
- qr_code_value
- notes
- created_by
- created_at
- updated_at

Status values:
- Draft
- Issued
- PartiallyPaid
- Paid
- Overdue
- Cancelled

---

## 9. Payment
Represents a payment against an invoice.

Fields:
- id
- invoice_id
- payment_date
- amount
- payment_method
- reference_number
- notes
- recorded_by
- created_at

Payment methods:
- Cash
- BankTransfer
- POS
- Online
- Other

---

## 10. TimeEntry
Tracks lawyer effort.

Fields:
- id
- case_id
- lawyer_id
- start_time
- end_time
- duration_minutes
- work_type
- notes
- created_at
- updated_at

Work types:
- Research
- Drafting
- Meeting
- CourtAttendance
- Review
- Communication
- Other

---

## 11. Notification
In-app notifications.

Fields:
- id
- user_id
- notification_type
- title
- message
- related_entity_type
- related_entity_id
- is_read
- created_at

Notification types:
- SessionReminder
- AppealDeadlineReminder
- POAExpiryReminder
- CaseDelayedWarning
- InvoiceOverdueAlert
- General

---

## 12. AuditLog
Tracks sensitive actions.

Fields:
- id
- user_id
- action
- entity_type
- entity_id
- description
- ip_address
- user_agent
- created_at

Tracked actions:
- CREATE
- UPDATE
- DELETE
- VIEW
- DOWNLOAD
- LOGIN
- LOGOUT

---

# Relationships

## Core Relationships
- Role 1 -> N User
- User (Client role) 1 -> 1 Client (optional portal account)
- Client 1 -> N PowerOfAttorney
- Client 1 -> N Case
- Lawyer (User with Lawyer role) 1 -> N Case
- Case 1 -> N CaseEvent
- Case 1 -> N Document
- Client 1 -> N Document
- Case 1 -> N Invoice
- Invoice 1 -> N Payment
- Case 1 -> N TimeEntry
- User 1 -> N Notification
- User 1 -> N AuditLog
- Case 1 -> N CaseAssignmentHistory

## Important Business Notes
- A client may have multiple cases.
- A lawyer may handle multiple cases.
- Each case has one primary assigned lawyer in MVP.
- Documents may belong to a case, a client, or both.
- A case may have multiple events and multiple invoices.
- A single invoice may be paid in multiple payments.
- PowerOfAttorney is separate from case because one client may reuse multiple agencies across different cases.