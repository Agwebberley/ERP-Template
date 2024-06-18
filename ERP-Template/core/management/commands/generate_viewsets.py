from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Generate viewsets for each model in each app'

    def handle(self, *args, **kwargs):
        app_configs = apps.get_app_configs()
        for app_config in app_configs:
            app_label = app_config.label
            # Check if in INGORED_APPS
            if app_label in getattr(settings, 'IGNORED_APPS', []):
                continue
            views_dir = os.path.join(app_label, 'views')
            os.makedirs(views_dir, exist_ok=True)

            app_models = app_config.get_models()
            for model in app_models:
                model_name = model.__name__
                viewset_content = f'''
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from {app_label}.models import {model_name}
from {app_label}.serializers.{model_name.lower()}_serializer import {model_name}Serializer

class {model_name}ViewSet(viewsets.ModelViewSet):
    queryset = {model_name}.objects.all()
    serializer_class = {model_name}Serializer
    permission_classes = [IsAuthenticated]

'''
                with open(os.path.join(views_dir, f'{model_name.lower()}_viewset.py'), 'w') as f:
                    f.write(viewset_content)

        self.stdout.write(self.style.SUCCESS('Successfully generated viewsets'))
