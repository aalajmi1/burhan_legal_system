from django.core.management.base import BaseCommand
from app.models import Client, Case, Invoice

class Command(BaseCommand):
    help = "Seed demo data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding demo data...")

        # Clients
        for i in range(1, 6):
            Client.objects.get_or_create(
                name=f"عميل {i}",
                email=f"client{i}@demo.com"
            )

        clients = Client.objects.all()

        # Cases
        for i in range(1, 6):
            Case.objects.get_or_create(
                title=f"قضية رقم {i}",
                client=clients[i-1]
            )

        cases = Case.objects.all()

        # Invoices
        for i in range(1, 6):
            Invoice.objects.get_or_create(
                case=cases[i-1],
                amount=1000 * i,
                description=f"فاتورة رقم {i}"
            )

        self.stdout.write(self.style.SUCCESS("Demo data created successfully"))
