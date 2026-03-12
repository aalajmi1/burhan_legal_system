from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from cases.models import Case
from clients.models import Client


class DocumentType(models.TextChoices):
    POWER_OF_ATTORNEY = "PowerOfAttorney", _("Power Of Attorney")
    JUDGMENT = "Judgment", _("Judgment")
    LEGAL_MEMO = "LegalMemo", _("Legal Memo")
    APPEAL_MEMO = "AppealMemo", _("Appeal Memo")
    CONTRACT = "Contract", _("Contract")
    EVIDENCE = "Evidence", _("Evidence")
    EXPERT_REPORT = "ExpertReport", _("Expert Report")
    IDENTITY_DOCUMENT = "IdentityDocument", _("Identity Document")
    INVOICE_ATTACHMENT = "InvoiceAttachment", _("Invoice Attachment")
    RECEIPT = "Receipt", _("Receipt")
    COURT_NOTICE = "CourtNotice", _("Court Notice")
    SESSION_MINUTES = "SessionMinutes", _("Session Minutes")
    OTHER = "Other", _("Other")


class Document(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="documents",
        null=True,
        blank=True,
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="documents",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255)
    document_type = models.CharField(
        max_length=40,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
    )
    file = models.FileField(upload_to="documents/")
    file_name = models.CharField(max_length=255, blank=True)
    file_size = models.PositiveIntegerField(default=0)
    mime_type = models.CharField(max_length=100, blank=True)
    version = models.PositiveIntegerField(default=1)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="uploaded_documents",
    )
    is_confidential = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    def save(self, *args, **kwargs):
        if self.file:
            self.file_name = self.file.name.split("/")[-1]
            try:
                self.file_size = self.file.size
            except Exception:
                pass
            if hasattr(self.file, "file") and hasattr(self.file.file, "content_type"):
                self.mime_type = self.file.file.content_type or ""
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title