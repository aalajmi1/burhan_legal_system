# TASKS.md

## Phase 1 - Backend Foundation
- Create Django project
- Configure PostgreSQL
- Configure DRF
- Configure JWT auth
- Create custom User model with roles
- Setup Docker Compose
- Setup Redis
- Setup Celery
- Setup base apps structure

## Phase 2 - Core Data Models
- Implement Client model
- Implement PowerOfAttorney model
- Implement Case model
- Implement CaseAssignmentHistory model
- Implement CaseEvent model
- Implement Document model
- Implement Invoice model
- Implement Payment model
- Implement TimeEntry model
- Implement Notification model
- Implement AuditLog model
- Create migrations
- Register all models in Django admin

## Phase 3 - API Layer
- Authentication APIs
- Users APIs
- Clients APIs
- POA APIs
- Cases APIs
- Case Events APIs
- Documents APIs
- Invoices APIs
- Payments APIs
- Notifications APIs
- Dashboard summary APIs

## Phase 4 - Permissions and Validation
- Admin full access
- Lawyer limited to assigned cases
- Client limited to own records
- Enforce role-based permissions
- Add object-level checks
- Add serializer validations

## Phase 5 - Business Rules
- Implement notification rules
- Implement invoice overdue update
- Implement delayed case logic
- Implement urgent case logic
- Implement appeal deadline reminders

## Phase 6 - Testing
- Authentication tests
- Permission tests
- CRUD tests
- Business rules tests
- Notification tests

## Phase 7 - Frontend
- Login page
- Admin dashboard
- Lawyer dashboard
- Client dashboard
- Clients pages
- Cases pages
- Documents pages
- Invoices pages
- Notifications center

## Phase 8 - Review and Hardening
- Review permissions
- Review validations
- Review API consistency
- Review audit logging coverage
- Review deployment files