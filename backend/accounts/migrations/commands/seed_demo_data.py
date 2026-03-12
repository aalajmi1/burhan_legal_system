from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User, UserRole
from clients.models import Client, PowerOfAttorney, PowerOfAttorneyStatus, IdentityType
from cases.models import (
    Case,
    CaseAssignmentHistory,
    CaseEvent,
    CaseEventType,
    CasePriority,
    CaseStatus,
    CaseType,
)


class Command(BaseCommand):
    help = "Seed demo data for Burhan legal system"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding demo data..."))

        # -------------------------
        # Users
        # -------------------------
        lawyer_1, _ = User.objects.get_or_create(
            email="lawyer1@burhan.sa",
            defaults={
                "full_name": "Ahmed Alqahtani",
                "role": UserRole.LAWYER,
                "is_active": True,
                "is_staff": True,
            },
        )
        lawyer_1.set_password("Lawyer123!")
        lawyer_1.save()

        lawyer_2, _ = User.objects.get_or_create(
            email="lawyer2@burhan.sa",
            defaults={
                "full_name": "Sara Alharbi",
                "role": UserRole.LAWYER,
                "is_active": True,
                "is_staff": True,
            },
        )
        lawyer_2.set_password("Lawyer123!")
        lawyer_2.save()

        client_user_1, _ = User.objects.get_or_create(
            email="client1@burhan.sa",
            defaults={
                "full_name": "Fahad Alotaibi",
                "role": UserRole.CLIENT,
                "is_active": True,
                "is_staff": False,
            },
        )
        client_user_1.set_password("Client123!")
        client_user_1.save()

        client_user_2, _ = User.objects.get_or_create(
            email="client2@burhan.sa",
            defaults={
                "full_name": "Maha Alshehri",
                "role": UserRole.CLIENT,
                "is_active": True,
                "is_staff": False,
            },
        )
        client_user_2.set_password("Client123!")
        client_user_2.save()

        # -------------------------
        # Clients
        # -------------------------
        client_1, _ = Client.objects.get_or_create(
            identity_number="1023456789",
            defaults={
                "full_name": "Fahad Alotaibi",
                "identity_type": IdentityType.NATIONAL_ID,
                "phone": "0501111111",
                "email": "client1@burhan.sa",
                "address": "Riyadh",
                "iban": "SA0380000000608010167519",
                "notes": "Commercial dispute client",
                "portal_user": client_user_1,
            },
        )

        client_2, _ = Client.objects.get_or_create(
            identity_number="2234567890",
            defaults={
                "full_name": "Maha Alshehri",
                "identity_type": IdentityType.IQAMA,
                "phone": "0502222222",
                "email": "client2@burhan.sa",
                "address": "Jeddah",
                "iban": "SA4420000001234567891234",
                "notes": "Labor case client",
                "portal_user": client_user_2,
            },
        )

        client_3, _ = Client.objects.get_or_create(
            identity_number="1019876543",
            defaults={
                "full_name": "Abdullah Trading Co.",
                "identity_type": IdentityType.COMMERCIAL_REGISTRATION,
                "phone": "0115555555",
                "email": "legal@abdullahtrading.sa",
                "address": "Dammam",
                "iban": "SA5510000000000009876543",
                "notes": "Corporate client",
                "portal_user": None,
            },
        )

        # -------------------------
        # Power of Attorneys
        # -------------------------
        poa_1, _ = PowerOfAttorney.objects.get_or_create(
            client=client_1,
            agency_number="NAJ-2026-0001",
            defaults={
                "issue_date": date.today() - timedelta(days=40),
                "expiry_date": date.today() + timedelta(days=180),
                "status": PowerOfAttorneyStatus.ACTIVE,
                "notes": "General litigation authority",
            },
        )

        poa_2, _ = PowerOfAttorney.objects.get_or_create(
            client=client_2,
            agency_number="NAJ-2026-0002",
            defaults={
                "issue_date": date.today() - timedelta(days=20),
                "expiry_date": date.today() + timedelta(days=25),
                "status": PowerOfAttorneyStatus.ACTIVE,
                "notes": "Labor court authority",
            },
        )

        poa_3, _ = PowerOfAttorney.objects.get_or_create(
            client=client_3,
            agency_number="NAJ-2026-0003",
            defaults={
                "issue_date": date.today() - timedelta(days=60),
                "expiry_date": date.today() + timedelta(days=365),
                "status": PowerOfAttorneyStatus.ACTIVE,
                "notes": "Commercial contract dispute authority",
            },
        )

        # -------------------------
        # Cases
        # -------------------------
        case_1, _ = Case.objects.get_or_create(
            case_number="COM-2026-1001",
            defaults={
                "title": "Commercial Contract Breach",
                "case_type": CaseType.COMMERCIAL,
                "court_name": "Commercial Court - Riyadh",
                "court_circuit": "Third Commercial Circuit",
                "status": CaseStatus.IN_PROGRESS,
                "priority": CasePriority.IMPORTANT,
                "description": "Claim for breach of contract and compensation.",
                "client": client_1,
                "assigned_lawyer": lawyer_1,
                "power_of_attorney": poa_1,
                "filing_date": date.today() - timedelta(days=15),
                "expected_close_date": date.today() + timedelta(days=120),
                "last_activity_at": timezone.now(),
            },
        )

        case_2, _ = Case.objects.get_or_create(
            case_number="LAB-2026-2001",
            defaults={
                "title": "Unpaid Salary and Benefits",
                "case_type": CaseType.LABOR,
                "court_name": "Labor Court - Jeddah",
                "court_circuit": "First Labor Circuit",
                "status": CaseStatus.WAITING_COURT_SESSION,
                "priority": CasePriority.URGENT,
                "description": "Labor dispute regarding delayed salary and end-of-service benefits.",
                "client": client_2,
                "assigned_lawyer": lawyer_2,
                "power_of_attorney": poa_2,
                "filing_date": date.today() - timedelta(days=7),
                "expected_close_date": date.today() + timedelta(days=60),
                "last_activity_at": timezone.now() - timedelta(days=2),
            },
        )

        case_3, _ = Case.objects.get_or_create(
            case_number="CIV-2026-3001",
            defaults={
                "title": "Property Damage Claim",
                "case_type": CaseType.CIVIL,
                "court_name": "General Court - Dammam",
                "court_circuit": "Second Civil Circuit",
                "status": CaseStatus.WAITING_JUDGMENT,
                "priority": CasePriority.NORMAL,
                "description": "Civil claim for damages caused to commercial property.",
                "client": client_3,
                "assigned_lawyer": lawyer_1,
                "power_of_attorney": poa_3,
                "filing_date": date.today() - timedelta(days=45),
                "expected_close_date": date.today() + timedelta(days=30),
                "last_activity_at": timezone.now() - timedelta(days=8),
            },
        )

        case_4, _ = Case.objects.get_or_create(
            case_number="ENF-2026-4001",
            defaults={
                "title": "Execution of Final Judgment",
                "case_type": CaseType.ENFORCEMENT,
                "court_name": "Enforcement Court - Riyadh",
                "court_circuit": "Execution Circuit 1",
                "status": CaseStatus.IN_ENFORCEMENT,
                "priority": CasePriority.IMPORTANT,
                "description": "Execution file for a previously issued final judgment.",
                "client": client_1,
                "assigned_lawyer": lawyer_2,
                "power_of_attorney": poa_1,
                "filing_date": date.today() - timedelta(days=90),
                "expected_close_date": date.today() + timedelta(days=45),
                "last_activity_at": timezone.now() - timedelta(days=1),
            },
        )

        # -------------------------
        # Assignment History
        # -------------------------
        CaseAssignmentHistory.objects.get_or_create(
            case=case_1,
            lawyer=lawyer_1,
            assigned_from=timezone.now() - timedelta(days=15),
            defaults={
                "assigned_to": None,
                "assigned_by": lawyer_1,
                "notes": "Initial assignment",
            },
        )

        CaseAssignmentHistory.objects.get_or_create(
            case=case_2,
            lawyer=lawyer_2,
            assigned_from=timezone.now() - timedelta(days=7),
            defaults={
                "assigned_to": None,
                "assigned_by": lawyer_2,
                "notes": "Initial assignment",
            },
        )

        # -------------------------
        # Case Events
        # -------------------------
        CaseEvent.objects.get_or_create(
            case=case_1,
            title="Initial Client Meeting",
            defaults={
                "event_type": CaseEventType.CLIENT_MEETING,
                "description": "Gathered contract documents and background details.",
                "event_date": timezone.now() - timedelta(days=14),
                "is_completed": True,
                "created_by": lawyer_1,
            },
        )

        CaseEvent.objects.get_or_create(
            case=case_1,
            title="Commercial Court Session",
            defaults={
                "event_type": CaseEventType.COURT_SESSION,
                "description": "First hearing before the commercial circuit.",
                "event_date": timezone.now() + timedelta(days=2),
                "is_completed": False,
                "created_by": lawyer_1,
            },
        )

        CaseEvent.objects.get_or_create(
            case=case_2,
            title="Appeal Deadline",
            defaults={
                "event_type": CaseEventType.APPEAL_DEADLINE,
                "description": "Final day to submit appeal memo if needed.",
                "event_date": timezone.now() + timedelta(days=4),
                "is_completed": False,
                "created_by": lawyer_2,
            },
        )

        CaseEvent.objects.get_or_create(
            case=case_2,
            title="Labor Court Session",
            defaults={
                "event_type": CaseEventType.COURT_SESSION,
                "description": "Upcoming labor case hearing.",
                "event_date": timezone.now() + timedelta(days=1),
                "is_completed": False,
                "created_by": lawyer_2,
            },
        )

        CaseEvent.objects.get_or_create(
            case=case_3,
            title="Judgment Expected",
            defaults={
                "event_type": CaseEventType.JUDGMENT_ISSUED,
                "description": "Court expected to issue judgment soon.",
                "event_date": timezone.now() + timedelta(days=5),
                "is_completed": False,
                "created_by": lawyer_1,
            },
        )

        CaseEvent.objects.get_or_create(
            case=case_4,
            title="Execution Action Follow-up",
            defaults={
                "event_type": CaseEventType.ENFORCEMENT_ACTION,
                "description": "Follow up with enforcement court on payment order.",
                "event_date": timezone.now() + timedelta(days=3),
                "is_completed": False,
                "created_by": lawyer_2,
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
        self.stdout.write("Lawyer login examples:")
        self.stdout.write(" - lawyer1@burhan.sa / Lawyer123!")
        self.stdout.write(" - lawyer2@burhan.sa / Lawyer123!")
        self.stdout.write("Client portal examples:")
        self.stdout.write(" - client1@burhan.sa / Client123!")
        self.stdout.write(" - client2@burhan.sa / Client123!")