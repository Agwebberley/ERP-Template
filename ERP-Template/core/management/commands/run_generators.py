from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    help = 'Run all generators'

    def handle(self, *args, **kwargs):
        subprocess.run(['python', 'manage.py', 'generate_serializers'])
        subprocess.run(['python', 'manage.py', 'generate_viewsets'])
        subprocess.run(['python', 'manage.py', 'generate_urls'])

        self.stdout.write(self.style.SUCCESS('Successfully ran all generators'))
