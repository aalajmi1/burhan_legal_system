from django.contrib import admin

from .models import Client, PowerOfAttorney


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "identity_type", "identity_number", "phone", "email")
    search_fields = ("full_name", "identity_number", "phone", "email")
    list_filter = ("identity_type",)
    ordering = ("id",)


@admin.register(PowerOfAttorney)
class PowerOfAttorneyAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "agency_number", "issue_date", "expiry_date", "status")
    search_fields = ("agency_number", "client__full_name", "client__identity_number")
    list_filter = ("status",)
    ordering = ("id",)