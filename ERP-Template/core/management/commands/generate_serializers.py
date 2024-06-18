from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Generate serializers for each model in each app'

    def handle(self, *args, **kwargs):
        app_configs = apps.get_app_configs()
        for app_config in app_configs:
            app_label = app_config.label
            # Check if in INGORED_APPS
            if app_label in getattr(settings, 'IGNORED_APPS', []):
                continue
            serializer_dir = os.path.join(app_label, 'serializers')
            os.makedirs(serializer_dir, exist_ok=True)

            app_models = app_config.get_models()
            for model in app_models:
                model_name = model.__name__
                serializer_content = f'''
from rest_framework import serializers
from {app_label}.models import {model_name}

class {model_name}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {model_name}
        fields = '__all__'
'''
                with open(os.path.join(serializer_dir, f'{model_name.lower()}_serializer.py'), 'w') as f:
                    f.write(serializer_content)

        self.stdout.write(self.style.SUCCESS('Successfully generated serializers'))
