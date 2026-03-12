from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from cases.models import Case
from clients.models import Client


class InvoiceStatus(models.TextChoices):
    DRAFT = "Draft", _("Draft")
    ISSUED = "Issued", _("Issued")
    PARTIALLY_PAID = "PartiallyPaid", _("Partially Paid")
    PAID = "Paid", _("Paid")
    OVERDUE = "Overdue", _("Overdue")
    CANCELLED = "Cancelled", _("Cancelled")


class PaymentMethod(models.TextChoices):
    CASH = "Cash", _("Cash")
    BANK_TRANSFER = "BankTransfer", _("Bank Transfer")
    POS = "POS", _("POS")
    ONLINE = "Online", _("Online")
    OTHER = "Other", _("Other")


class WorkType(models.TextChoices):
    RESEARCH = "Research", _("Research")
    DRAFTING = "Drafting", _("Drafting")
    MEETING = "Meeting", _("Meeting")
    COURT_ATTENDANCE = "CourtAttendance", _("Court Attendance")
    REVIEW = "Review", _("Review")
    COMMUNICATION = "Communication", _("Communication")
    OTHER = "Other", _("Other")


class Invoice(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="invoices",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="invoices",
    )
    invoice_number = models.CharField(max_length=100, unique=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    fees_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    government_fees_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    court_costs_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.DRAFT,
    )
    qr_code_value = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_invoices",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    def save(self, *args, **kwargs):
        self.total_amount = (
            self.fees_amount
            + self.government_fees_amount
            + self.court_costs_amount
            + self.tax_amount
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number


class Payment(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.BANK_TRANSFER,
    )
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="recorded_payments",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.amount}"


class TimeEntry(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="time_entries",
    )
    lawyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="time_entries",
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=0)
    work_type = models.CharField(
        max_length=30,
        choices=WorkType.choices,
        default=WorkType.OTHER,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Time Entry")
        verbose_name_plural = _("Time Entries")

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.duration_minutes = int(delta.total_seconds() // 60)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.case.case_number} - {self.lawyer.full_name}"