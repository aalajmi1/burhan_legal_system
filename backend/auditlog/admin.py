from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "action",
        "entity_type",
        "entity_id",
        "ip_address",
        "created_at",
    )
    search_fields = ("entity_type", "description", "user__email")
    list_filter = ("action",)
    ordering = ("-id",)