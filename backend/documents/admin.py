from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "document_type",
        "case",
        "client",
        "uploaded_by",
        "version",
        "is_confidential",
    )
    search_fields = ("title", "case__case_number", "client__full_name")
    list_filter = ("document_type", "is_confidential")
    ordering = ("id",)