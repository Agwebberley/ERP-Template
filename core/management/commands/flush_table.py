from django.core.management.base import BaseCommand
from core.models import LogMessage


class Command(BaseCommand):
    help = "Flushes the YourModel table"

    def handle(self, *args, **options):
        LogMessage.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS("Successfully flushed the YourModel table.")
        )
