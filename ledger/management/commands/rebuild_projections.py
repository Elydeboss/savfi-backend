from django.core.management.base import BaseCommand
from ledger.models import Event, WalletProjection, DepositProjection
from ledger.projections import apply_event_to_projections
from django.db import transaction

class Command(BaseCommand):
    help = "Rebuild all projections by replaying events"

    def handle(self, *args, **options):
        self.stdout.write("Clearing projections...")
        WalletProjection.objects.all().delete()
        DepositProjection.objects.all().delete()

        events = Event.objects.order_by("created_at", "version").iterator()
        count = 0
        for ev in events:
            apply_event_to_projections(ev)
            count += 1
            if count % 1000 == 0:
                self.stdout.write(f"Applied {count} events")
        self.stdout.write(self.style.SUCCESS(f"Applied {count} events"))
