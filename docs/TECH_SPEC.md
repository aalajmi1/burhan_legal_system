# TECH_SPEC.md

## Project
Burhan Legal System (MVP)

## Objective
A secure legal office management system tailored for Saudi legal workflows, including case management, client records, legal calendar, document vault, invoicing, notifications, and dashboards for Admin, Lawyer, and Client.

## Final Technical Stack

### Backend
- Python 3.12
- Django
- Django REST Framework
- djangorestframework-simplejwt

### Database
- PostgreSQL

### Async / Scheduled Jobs
- Celery
- Redis

### Frontend
- Next.js (implemented later, after backend stabilization)

### File Storage
- Private local media storage for MVP
- Future option: MinIO / S3-compatible object storage

### Authentication
- JWT authentication
- Role-based access control (RBAC)

### Deployment
- Docker Compose for local development
- Ubuntu + Docker + Nginx for deployment

## Core Backend Modules
1. Authentication
2. Users & Roles
3. Clients
4. Cases
5. Case Events
6. Documents
7. Invoices
8. Payments
9. Time Tracking
10. Notifications
11. Audit Logs

## Security Requirements
- HTTPS/TLS in deployment
- Hashed passwords using Django defaults
- Role-based access restrictions
- File access only through authenticated authorized users
- Audit logging for create/update/delete/download actions
- Input validation on all APIs

## MVP Scope
Included in MVP:
- JWT login
- Admin / Lawyer / Client roles
- Client management
- Case management
- Case events
- Document upload
- Invoice and payment records
- In-app notifications
- Basic audit logs
- Lawyer dashboard
- Client dashboard
- Admin dashboard

Deferred to later versions:
- Direct Najiz integration
- Deep ZATCA Phase 2 integration
- OCR extraction
- AI legal drafting
- WhatsApp integration
- Advanced analytics