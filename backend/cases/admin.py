from django.contrib import admin

from .models import Case, CaseAssignmentHistory, CaseEvent


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ("id", "case_number", "title", "case_type", "status", "priority", "client", "assigned_lawyer")
    search_fields = ("case_number", "title", "client__full_name", "assigned_lawyer__full_name")
    list_filter = ("case_type", "status", "priority")
    ordering = ("id",)


@admin.register(CaseAssignmentHistory)
class CaseAssignmentHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "case", "lawyer", "assigned_from", "assigned_to", "assigned_by")
    search_fields = ("case__case_number", "lawyer__full_name", "assigned_by__full_name")
    ordering = ("id",)


@admin.register(CaseEvent)
class CaseEventAdmin(admin.ModelAdmin):
    list_display = ("id", "case", "event_type", "title", "event_date", "is_completed", "created_by")
    search_fields = ("case__case_number", "title", "created_by__full_name")
    list_filter = ("event_type", "is_completed")
    ordering = ("id",)