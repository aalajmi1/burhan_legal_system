from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class IdentityType(models.TextChoices):
    NATIONAL_ID = "NationalID", _("National ID")
    IQAMA = "Iqama", _("Iqama")
    COMMERCIAL_REGISTRATION = "CommercialRegistration", _("Commercial Registration")
    PASSPORT = "Passport", _("Passport")
    OTHER = "Other", _("Other")


class Client(models.Model):
    full_name = models.CharField(max_length=255)
    identity_type = models.CharField(
        max_length=30,
        choices=IdentityType.choices,
        default=IdentityType.NATIONAL_ID,
    )
    identity_number = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    iban = models.CharField(max_length=34, blank=True)
    notes = models.TextField(blank=True)
    portal_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_profile",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self):
        return f"{self.full_name} - {self.identity_number}"


class PowerOfAttorneyStatus(models.TextChoices):
    ACTIVE = "Active", _("Active")
    EXPIRED = "Expired", _("Expired")
    REVOKED = "Revoked", _("Revoked")
    PENDING_VERIFICATION = "PendingVerification", _("Pending Verification")


class PowerOfAttorney(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="power_of_attorneys",
    )
    agency_number = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(
        max_length=30,
        choices=PowerOfAttorneyStatus.choices,
        default=PowerOfAttorneyStatus.ACTIVE,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Power of Attorney")
        verbose_name_plural = _("Power of Attorneys")
        unique_together = ("client", "agency_number")

    def __str__(self):
        return f"{self.client.full_name} - {self.agency_number}"