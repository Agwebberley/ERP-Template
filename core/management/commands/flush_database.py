from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = "Flushes the entire database"

    def handle(self, *args, **options):
        for connection in connections.all():
            connection.cursor().execute(
                "DROP DATABASE " + connection.settings_dict["NAME"]
            )
        self.stdout.write(self.style.SUCCESS("Database flushed successfully."))
