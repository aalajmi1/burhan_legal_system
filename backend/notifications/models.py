from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationType(models.TextChoices):
    SESSION_REMINDER = "SessionReminder", _("Session Reminder")
    APPEAL_DEADLINE_REMINDER = "AppealDeadlineReminder", _("Appeal Deadline Reminder")
    POA_EXPIRY_REMINDER = "POAExpiryReminder", _("POA Expiry Reminder")
    CASE_DELAYED_WARNING = "CaseDelayedWarning", _("Case Delayed Warning")
    INVOICE_OVERDUE_ALERT = "InvoiceOverdueAlert", _("Invoice Overdue Alert")
    GENERAL = "General", _("General")


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    notification_type = models.CharField(
        max_length=40,
        choices=NotificationType.choices,
        default=NotificationType.GENERAL,
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_entity_type = models.CharField(max_length=100, blank=True)
    related_entity_id = models.PositiveIntegerField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return self.title