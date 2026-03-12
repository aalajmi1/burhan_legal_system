from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from clients.models import Client, PowerOfAttorney


class CaseType(models.TextChoices):
    COMMERCIAL = "Commercial", _("Commercial")
    CIVIL = "Civil", _("Civil")
    CRIMINAL = "Criminal", _("Criminal")
    LABOR = "Labor", _("Labor")
    FAMILY = "Family", _("Family")
    REAL_ESTATE = "RealEstate", _("Real Estate")
    ENFORCEMENT = "Enforcement", _("Enforcement")
    ADMINISTRATIVE = "Administrative", _("Administrative")
    OTHER = "Other", _("Other")


class CasePriority(models.TextChoices):
    URGENT = "Urgent", _("Urgent")
    IMPORTANT = "Important", _("Important")
    NORMAL = "Normal", _("Normal")


class CaseStatus(models.TextChoices):
    NEW = "New", _("New")
    IN_PROGRESS = "InProgress", _("In Progress")
    WAITING_COURT_SESSION = "WaitingCourtSession", _("Waiting Court Session")
    WAITING_JUDGMENT = "WaitingJudgment", _("Waiting Judgment")
    JUDGMENT_ISSUED = "JudgmentIssued", _("Judgment Issued")
    UNDER_APPEAL = "UnderAppeal", _("Under Appeal")
    IN_ENFORCEMENT = "InEnforcement", _("In Enforcement")
    SUSPENDED = "Suspended", _("Suspended")
    CLOSED = "Closed", _("Closed")


class Case(models.Model):
    case_number = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    case_type = models.CharField(
        max_length=30,
        choices=CaseType.choices,
        default=CaseType.OTHER,
    )
    court_name = models.CharField(max_length=255)
    court_circuit = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=30,
        choices=CaseStatus.choices,
        default=CaseStatus.NEW,
    )
    priority = models.CharField(
        max_length=20,
        choices=CasePriority.choices,
        default=CasePriority.NORMAL,
    )
    description = models.TextField(blank=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="cases",
    )
    assigned_lawyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="assigned_cases",
    )
    power_of_attorney = models.ForeignKey(
        PowerOfAttorney,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cases",
    )
    filing_date = models.DateField(null=True, blank=True)
    expected_close_date = models.DateField(null=True, blank=True)
    last_activity_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Case")
        verbose_name_plural = _("Cases")

    def __str__(self):
        return f"{self.case_number} - {self.title}"


class CaseAssignmentHistory(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="assignment_history",
    )
    lawyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="case_assignment_history",
    )
    assigned_from = models.DateTimeField()
    assigned_to = models.DateTimeField(null=True, blank=True)
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="case_assignments_made",
    )
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Case Assignment History")
        verbose_name_plural = _("Case Assignment Histories")

    def __str__(self):
        return f"{self.case.case_number} -> {self.lawyer.full_name}"


class CaseEventType(models.TextChoices):
    COURT_SESSION = "CourtSession", _("Court Session")
    APPEAL_DEADLINE = "AppealDeadline", _("Appeal Deadline")
    EXPERT_VISIT = "ExpertVisit", _("Expert Visit")
    CLIENT_MEETING = "ClientMeeting", _("Client Meeting")
    INTERNAL_REVIEW = "InternalReview", _("Internal Review")
    DOCUMENT_SUBMISSION = "DocumentSubmission", _("Document Submission")
    PAYMENT_DEADLINE = "PaymentDeadline", _("Payment Deadline")
    JUDGMENT_ISSUED = "JudgmentIssued", _("Judgment Issued")
    ENFORCEMENT_ACTION = "EnforcementAction", _("Enforcement Action")
    OTHER = "Other", _("Other")


class CaseEvent(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="events",
    )
    event_type = models.CharField(
        max_length=30,
        choices=CaseEventType.choices,
        default=CaseEventType.OTHER,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_case_events",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Case Event")
        verbose_name_plural = _("Case Events")

    def __str__(self):
        return f"{self.case.case_number} - {self.title}"