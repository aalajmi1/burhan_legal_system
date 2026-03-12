# PRD.md

# Burhan Legal System (MVP)
Saudi Legal Office Management System

## Vision
Build a secure centralized system for Saudi legal offices to replace fragmented workflows using Excel, shared folders, and manual tracking. The system must support lawyers, clients, and administrators with strong access control, legal case workflows, financial tracking, and operational transparency.

## Main Goals
- Centralize legal office operations
- Secure client and case data
- Improve lawyer productivity
- Provide client transparency
- Track legal deadlines and sessions
- Improve billing and collections
- Maintain auditability

## User Roles

### Admin
- Full access to all data
- Manage users
- View office-wide reports
- Review financial records
- Review audit logs
- Monitor lawyer performance

### Lawyer
- Access assigned cases
- Update case status
- Upload legal documents
- Add case events
- Log work time
- View notifications

### Client
- Read-only access to own case updates
- View sessions and meetings
- Download invoices
- View latest updates

## Core Functional Requirements

### 1. Client Management
- Store full client information
- Support Saudi identity types
- Store IBAN
- Link portal account when needed

### 2. Power of Attorney Management
- Store agency number
- Track issue and expiry dates
- Alert before expiry
- Link agency to cases if needed

### 3. Case Management
- Create and update cases
- Assign a lawyer
- Track case type and court
- Track status and priority
- Maintain case timeline

### 4. Case Timeline / Events
- Add court sessions
- Add appeal deadlines
- Add expert visits
- Add client meetings
- Add internal review events

### 5. Document Vault
- Upload and categorize documents
- Support versioning
- Link documents to case/client
- Restrict access based on permissions

### 6. Financial Management
- Create invoices
- Distinguish fees vs government costs
- Record payments
- Track overdue invoices

### 7. Time Tracking
- Start/stop or manually record lawyer effort
- Store duration and work type
- Report effort per case

### 8. Notifications
- Show in-app notifications
- Alert for near sessions
- Alert for appeal deadlines
- Alert for POA expiry
- Alert for overdue invoices
- Alert for delayed inactive cases

### 9. Audit Logging
- Log sensitive operations
- Track who did what and when
- Track source device/IP when possible

## Dashboards

### Admin Dashboard
- Active cases count
- Cases by status
- Overdue invoices
- Lawyers performance summary
- Recent audit actions

### Lawyer Dashboard
- Today sessions
- Assigned cases
- Urgent deadlines
- Delayed cases
- Unread notifications

### Client Dashboard
- My cases
- Upcoming sessions
- Latest updates
- My invoices

## Case Status Definitions
- New
- InProgress
- WaitingCourtSession
- WaitingJudgment
- JudgmentIssued
- UnderAppeal
- InEnforcement
- Suspended
- Closed

## Document Types
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

## Notification Rules

### Rule 1: Upcoming Court Session
If a case has a CourtSession event within 48 hours:
- mark case as Urgent
- notify assigned lawyer

### Rule 2: Missing Memo Before Session
If a court session is within 3 days and no LegalMemo or AppealMemo exists:
- notify assigned lawyer with warning

### Rule 3: Power of Attorney Expiry
If POA expiry date is within 30 days:
- notify assigned lawyer
- notify admin

### Rule 4: Inactive Case
If case last activity is older than 7 days and case is not Closed:
- show in delayed cases list for lawyer
- notify lawyer

### Rule 5: Overdue Invoice
If invoice due date has passed and status is not Paid:
- mark invoice as Overdue
- notify admin

### Rule 6: Appeal Deadline
If an AppealDeadline event is within 5 days:
- notify assigned lawyer daily

## Out of Scope for MVP
- Direct Najiz integration
- Full ZATCA Phase 2 integration
- OCR extraction from uploaded PDFs
- AI drafting assistant
- WhatsApp integration
- Advanced BI analytics