from django.contrib import admin

from .models import Invoice, Payment, TimeEntry


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "invoice_number",
        "case",
        "client",
        "issue_date",
        "due_date",
        "total_amount",
        "status",
    )
    search_fields = ("invoice_number", "case__case_number", "client__full_name")
    list_filter = ("status",)
    ordering = ("id",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "invoice",
        "payment_date",
        "amount",
        "payment_method",
        "recorded_by",
    )
    search_fields = ("invoice__invoice_number", "reference_number")
    list_filter = ("payment_method",)
    ordering = ("id",)


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "case",
        "lawyer",
        "work_type",
        "start_time",
        "end_time",
        "duration_minutes",
    )
    search_fields = ("case__case_number", "lawyer__full_name")
    list_filter = ("work_type",)
    ordering = ("id",)