from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class AuditAction(models.TextChoices):
    CREATE = "CREATE", _("CREATE")
    UPDATE = "UPDATE", _("UPDATE")
    DELETE = "DELETE", _("DELETE")
    VIEW = "VIEW", _("VIEW")
    DOWNLOAD = "DOWNLOAD", _("DOWNLOAD")
    LOGIN = "LOGIN", _("LOGIN")
    LOGOUT = "LOGOUT", _("LOGOUT")


class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    action = models.CharField(
        max_length=20,
        choices=AuditAction.choices,
    )
    entity_type = models.CharField(max_length=100)
    entity_id = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Audit Log")
        verbose_name_plural = _("Audit Logs")

    def __str__(self):
        return f"{self.action} - {self.entity_type} - {self.created_at}"