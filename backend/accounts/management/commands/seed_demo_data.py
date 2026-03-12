from datetime import date, timedelta
from decimal import Decimal

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User, UserRole
from auditlog.models import AuditAction, AuditLog
from cases.models import (
    Case,
    CaseAssignmentHistory,
    CaseEvent,
    CaseEventType,
    CasePriority,
    CaseStatus,
    CaseType,
)
from clients.models import Client, IdentityType, PowerOfAttorney, PowerOfAttorneyStatus
from documents.models import Document, DocumentType
from finance.models import Invoice, InvoiceStatus, Payment, PaymentMethod, TimeEntry, WorkType
from notifications.models import Notification, NotificationType


class Command(BaseCommand):
    help = "زرع بيانات تجريبية عربية لنظام برهان"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("جاري إدخال البيانات العربية التجريبية..."))

        # =========================
        # المستخدمون
        # =========================
        lawyer_1, _ = User.objects.get_or_create(
            email="lawyer1@burhan.sa",
            defaults={
                "full_name": "أحمد القحطاني",
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
                "full_name": "سارة الحربي",
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
                "full_name": "فهد العتيبي",
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
                "full_name": "مها الشهري",
                "role": UserRole.CLIENT,
                "is_active": True,
                "is_staff": False,
            },
        )
        client_user_2.set_password("Client123!")
        client_user_2.save()

        # =========================
        # العملاء
        # =========================
        client_1, _ = Client.objects.get_or_create(
            identity_number="1023456789",
            defaults={
                "full_name": "فهد العتيبي",
                "identity_type": IdentityType.NATIONAL_ID,
                "phone": "0501111111",
                "email": "client1@burhan.sa",
                "address": "الرياض",
                "iban": "SA0380000000608010167519",
                "notes": "عميل في نزاع تجاري",
                "portal_user": client_user_1,
            },
        )

        client_2, _ = Client.objects.get_or_create(
            identity_number="2234567890",
            defaults={
                "full_name": "مها الشهري",
                "identity_type": IdentityType.IQAMA,
                "phone": "0502222222",
                "email": "client2@burhan.sa",
                "address": "جدة",
                "iban": "SA4420000001234567891234",
                "notes": "عميلة في قضية عمالية",
                "portal_user": client_user_2,
            },
        )

        client_3, _ = Client.objects.get_or_create(
            identity_number="1019876543",
            defaults={
                "full_name": "شركة عبدالله للتجارة",
                "identity_type": IdentityType.COMMERCIAL_REGISTRATION,
                "phone": "0115555555",
                "email": "legal@abdullahtrading.sa",
                "address": "الدمام",
                "iban": "SA5510000000000009876543",
                "notes": "عميل مؤسسي",
            },
        )

        # =========================
        # الوكالات
        # =========================
        poa_1, _ = PowerOfAttorney.objects.get_or_create(
            client=client_1,
            agency_number="NAJ-2026-0001",
            defaults={
                "issue_date": date.today() - timedelta(days=40),
                "expiry_date": date.today() + timedelta(days=180),
                "status": PowerOfAttorneyStatus.ACTIVE,
                "notes": "وكالة عامة للترافع",
            },
        )

        poa_2, _ = PowerOfAttorney.objects.get_or_create(
            client=client_2,
            agency_number="NAJ-2026-0002",
            defaults={
                "issue_date": date.today() - timedelta(days=20),
                "expiry_date": date.today() + timedelta(days=25),
                "status": PowerOfAttorneyStatus.ACTIVE,
                "notes": "وكالة خاصة بالقضايا العمالية",
            },
        )

        poa_3, _ = PowerOfAttorney.objects.get_or_create(
            client=client_3,
            agency_number="NAJ-2026-0003",
            defaults={
                "issue_date": date.today() - timedelta(days=60),
                "expiry_date": date.today() + timedelta(days=365),
                "status": PowerOfAttorneyStatus.ACTIVE,
                "notes": "وكالة لنزاع عقود تجارية",
            },
        )

        # =========================
        # القضايا
        # =========================
        case_1, _ = Case.objects.get_or_create(
            case_number="COM-2026-1001",
            defaults={
                "title": "إخلال بعقد تجاري",
                "case_type": CaseType.COMMERCIAL,
                "court_name": "المحكمة التجارية - الرياض",
                "court_circuit": "الدائرة التجارية الثالثة",
                "status": CaseStatus.IN_PROGRESS,
                "priority": CasePriority.IMPORTANT,
                "description": "دعوى تعويض بسبب إخلال أحد الأطراف بالعقد التجاري.",
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
                "title": "مطالبة برواتب ومستحقات",
                "case_type": CaseType.LABOR,
                "court_name": "المحكمة العمالية - جدة",
                "court_circuit": "الدائرة العمالية الأولى",
                "status": CaseStatus.WAITING_COURT_SESSION,
                "priority": CasePriority.URGENT,
                "description": "نزاع عمالي بخصوص تأخر الرواتب ومكافأة نهاية الخدمة.",
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
                "title": "مطالبة بتعويض عن أضرار عقار",
                "case_type": CaseType.CIVIL,
                "court_name": "المحكمة العامة - الدمام",
                "court_circuit": "الدائرة الحقوقية الثانية",
                "status": CaseStatus.WAITING_JUDGMENT,
                "priority": CasePriority.NORMAL,
                "description": "دعوى مدنية للمطالبة بتعويض عن أضرار لحقت بعقار تجاري.",
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
                "title": "تنفيذ حكم نهائي",
                "case_type": CaseType.ENFORCEMENT,
                "court_name": "محكمة التنفيذ - الرياض",
                "court_circuit": "دائرة التنفيذ الأولى",
                "status": CaseStatus.IN_ENFORCEMENT,
                "priority": CasePriority.IMPORTANT,
                "description": "ملف تنفيذ لحكم نهائي صادر سابقًا.",
                "client": client_1,
                "assigned_lawyer": lawyer_2,
                "power_of_attorney": poa_1,
                "filing_date": date.today() - timedelta(days=90),
                "expected_close_date": date.today() + timedelta(days=45),
                "last_activity_at": timezone.now() - timedelta(days=1),
            },
        )

        # =========================
        # سجل توزيع القضايا
        # =========================
        CaseAssignmentHistory.objects.get_or_create(
            case=case_1,
            lawyer=lawyer_1,
            assigned_from=timezone.now() - timedelta(days=15),
            defaults={
                "assigned_to": None,
                "assigned_by": lawyer_1,
                "notes": "إسناد أولي للقضية",
            },
        )

        CaseAssignmentHistory.objects.get_or_create(
            case=case_2,
            lawyer=lawyer_2,
            assigned_from=timezone.now() - timedelta(days=7),
            defaults={
                "assigned_to": None,
                "assigned_by": lawyer_2,
                "notes": "إسناد أولي للقضية",
            },
        )

        # =========================
        # أحداث القضايا
        # =========================
        CaseEvent.objects.get_or_create(
            case=case_1,
            title="اجتماع أولي مع العميل",
            defaults={
                "event_type": CaseEventType.CLIENT_MEETING,
                "description": "تم جمع مستندات العقد وتفاصيل النزاع.",
                "event_date": timezone.now() - timedelta(days=14),
                "is_completed": True,
                "created_by": lawyer_1,
            },
        )

        CaseEvent.objects.get_or_create(
            case=case_1,
            title="جلسة المحكمة التجارية",
            defaults={
                "event_type": CaseEventType.COURT_SESSION,
                "description": "أول جلسة أمام الدائرة التجارية.",
                "event_date": timezone.now() + timedelta(days=2),
                "is_completed": False,
                "created_by": lawyer_1,
            },
        )

        CaseEvent.objects.get_or_create(
            case=case_2,
            title="مهلة الاعتراض",
            defaults={
                "event_type": CaseEventType.APPEAL_DEADLINE,
                "description": "آخر موعد لتقديم لائحة الاعتراض إذا لزم.",
                "event_date": timezone.now() + timedelta(days=4),
                "is_completed": False,
                "created_by": lawyer_2,
            },
        )

        CaseEvent.objects.get_or_create(
            case=case_2,
            title="جلسة المحكمة العمالية",
            defaults={
                "event_type": CaseEventType.COURT_SESSION,
                "description": "جلسة قريبة في القضية العمالية.",
                "event_date": timezone.now() + timedelta(days=1),
                "is_completed": False,
                "created_by": lawyer_2,
            },
        )

        CaseEvent.objects.get_or_create(
            case=case_3,
            title="موعد متوقع لصدور الحكم",
            defaults={
                "event_type": CaseEventType.JUDGMENT_ISSUED,
                "description": "المحكمة يتوقع أن تصدر الحكم قريبًا.",
                "event_date": timezone.now() + timedelta(days=5),
                "is_completed": False,
                "created_by": lawyer_1,
            },
        )

        CaseEvent.objects.get_or_create(
            case=case_4,
            title="متابعة إجراء التنفيذ",
            defaults={
                "event_type": CaseEventType.ENFORCEMENT_ACTION,
                "description": "متابعة مع محكمة التنفيذ بخصوص أمر السداد.",
                "event_date": timezone.now() + timedelta(days=3),
                "is_completed": False,
                "created_by": lawyer_2,
            },
        )

        # =========================
        # المستندات
        # =========================
        if not Document.objects.filter(title="نسخة العقد التجاري").exists():
            doc = Document(
                case=case_1,
                client=client_1,
                title="نسخة العقد التجاري",
                document_type=DocumentType.CONTRACT,
                uploaded_by=lawyer_1,
                notes="نسخة العقد الموقعة بين الطرفين",
            )
            doc.file.save("contract_ar.txt", ContentFile("هذه نسخة تجريبية لمحتوى العقد التجاري."), save=True)

        if not Document.objects.filter(title="مذكرة المطالبة العمالية").exists():
            doc = Document(
                case=case_2,
                client=client_2,
                title="مذكرة المطالبة العمالية",
                document_type=DocumentType.LEGAL_MEMO,
                uploaded_by=lawyer_2,
                notes="مذكرة أولية في النزاع العمالي",
            )
            doc.file.save("labor_memo_ar.txt", ContentFile("هذه مذكرة قانونية تجريبية باللغة العربية."), save=True)

        # =========================
        # الفواتير
        # =========================
        invoice_1, _ = Invoice.objects.get_or_create(
            invoice_number="INV-2026-0001",
            defaults={
                "case": case_1,
                "client": client_1,
                "issue_date": date.today() - timedelta(days=5),
                "due_date": date.today() + timedelta(days=10),
                "fees_amount": Decimal("5000.00"),
                "government_fees_amount": Decimal("500.00"),
                "court_costs_amount": Decimal("250.00"),
                "tax_amount": Decimal("862.50"),
                "status": InvoiceStatus.ISSUED,
                "qr_code_value": "QR-INV-2026-0001",
                "notes": "أتعاب أولية للقضية التجارية",
                "created_by": lawyer_1,
            },
        )

        invoice_2, _ = Invoice.objects.get_or_create(
            invoice_number="INV-2026-0002",
            defaults={
                "case": case_2,
                "client": client_2,
                "issue_date": date.today() - timedelta(days=15),
                "due_date": date.today() - timedelta(days=2),
                "fees_amount": Decimal("3500.00"),
                "government_fees_amount": Decimal("300.00"),
                "court_costs_amount": Decimal("150.00"),
                "tax_amount": Decimal("592.50"),
                "status": InvoiceStatus.OVERDUE,
                "qr_code_value": "QR-INV-2026-0002",
                "notes": "فاتورة أتعاب القضية العمالية",
                "created_by": lawyer_2,
            },
        )

        # =========================
        # المدفوعات
        # =========================
        Payment.objects.get_or_create(
            invoice=invoice_1,
            reference_number="PAY-2026-1001",
            defaults={
                "payment_date": date.today() - timedelta(days=1),
                "amount": Decimal("2000.00"),
                "payment_method": PaymentMethod.BANK_TRANSFER,
                "notes": "دفعة جزئية مستلمة",
                "recorded_by": lawyer_1,
            },
        )

        # =========================
        # تتبع الوقت
        # =========================
        TimeEntry.objects.get_or_create(
            case=case_1,
            lawyer=lawyer_1,
            start_time=timezone.now() - timedelta(hours=5),
            end_time=timezone.now() - timedelta(hours=3, minutes=30),
            defaults={
                "work_type": WorkType.DRAFTING,
                "notes": "إعداد مذكرة الإخلال بالعقد",
            },
        )

        TimeEntry.objects.get_or_create(
            case=case_2,
            lawyer=lawyer_2,
            start_time=timezone.now() - timedelta(hours=2),
            end_time=timezone.now() - timedelta(hours=1),
            defaults={
                "work_type": WorkType.MEETING,
                "notes": "اجتماع تشاوري مع العميلة",
            },
        )

        # =========================
        # الإشعارات
        # =========================
        Notification.objects.get_or_create(
            user=lawyer_1,
            title="تذكير بجلسة المحكمة التجارية",
            defaults={
                "notification_type": NotificationType.SESSION_REMINDER,
                "message": "القضية COM-2026-1001 لديها جلسة خلال 48 ساعة.",
                "related_entity_type": "Case",
                "related_entity_id": case_1.id,
                "is_read": False,
            },
        )

        Notification.objects.get_or_create(
            user=lawyer_2,
            title="تنبيه فاتورة متأخرة",
            defaults={
                "notification_type": NotificationType.INVOICE_OVERDUE_ALERT,
                "message": "الفاتورة INV-2026-0002 متأخرة عن السداد.",
                "related_entity_type": "Invoice",
                "related_entity_id": invoice_2.id,
                "is_read": False,
            },
        )

        Notification.objects.get_or_create(
            user=lawyer_2,
            title="تذكير قرب انتهاء الوكالة",
            defaults={
                "notification_type": NotificationType.POA_EXPIRY_REMINDER,
                "message": "الوكالة NAJ-2026-0002 ستنتهي خلال أقل من 30 يومًا.",
                "related_entity_type": "PowerOfAttorney",
                "related_entity_id": poa_2.id,
                "is_read": False,
            },
        )

        # =========================
        # سجل العمليات
        # =========================
        AuditLog.objects.get_or_create(
            user=lawyer_1,
            action=AuditAction.CREATE,
            entity_type="Case",
            entity_id=case_1.id,
            defaults={
                "description": "تم إنشاء القضية التجارية COM-2026-1001",
                "ip_address": "127.0.0.1",
                "user_agent": "seed_script",
            },
        )

        AuditLog.objects.get_or_create(
            user=lawyer_2,
            action=AuditAction.CREATE,
            entity_type="Invoice",
            entity_id=invoice_2.id,
            defaults={
                "description": "تم إنشاء الفاتورة المتأخرة INV-2026-0002",
                "ip_address": "127.0.0.1",
                "user_agent": "seed_script",
            },
        )

        self.stdout.write(self.style.SUCCESS("تم إدخال البيانات العربية التجريبية بنجاح."))
        self.stdout.write("حسابات المحامين:")
        self.stdout.write(" - lawyer1@burhan.sa / Lawyer123!")
        self.stdout.write(" - lawyer2@burhan.sa / Lawyer123!")
        self.stdout.write("حسابات العملاء:")
        self.stdout.write(" - client1@burhan.sa / Client123!")
        self.stdout.write(" - client2@burhan.sa / Client123!")