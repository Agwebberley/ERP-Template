from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
import os
import json

class Command(BaseCommand):
    help = 'Generate serializers for each model in each app'

    def handle(self, *args, **kwargs):
        # Load configuration file
        config_file_path = os.path.join(settings.BASE_DIR, 'serializer_config.json')
        if not os.path.exists(config_file_path):
            self.stdout.write(self.style.ERROR('Configuration file not found: serializer_config.json'))
            return
        
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)

        app_configs = apps.get_app_configs()
        for app_config in app_configs:
            app_label = app_config.label
            if app_label in getattr(settings, 'IGNORED_APPS', []):
                continue

            serializer_dir = os.path.join(app_label, 'serializers')
            os.makedirs(serializer_dir, exist_ok=True)

            app_models = app_config.get_models()
            for model in app_models:
                model_name = model.__name__
                model_key = f"{app_label}.{model_name}"
                nested_fields = config.get(model_key, [])
                
                nested_serializers = ""
                nested_fields_code = ""

                if nested_fields:
                    related_fields = [f for f in model._meta.get_fields() if f.one_to_many or f.one_to_one]
                    
                    for field in related_fields:
                        if field.name in nested_fields:
                            related_app_label = field.related_model._meta.app_label
                            related_model = field.related_model
                            related_model_name = related_model.__name__
                            nested_serializers += f"\nfrom {related_app_label}.models import {related_model_name}\n"
                            nested_serializer_name = f"{related_model_name}Serializer"
                            nested_serializers += f"\n\nclass {nested_serializer_name}(serializers.ModelSerializer):\n"
                            nested_serializers += f"    class Meta:\n"
                            nested_serializers += f"        model = {related_model_name}\n"
                            nested_serializers += f"        fields = '__all__'\n"
                            nested_fields_code += f"    {field.name} = {nested_serializer_name}(many=True, read_only=True)\n"

                serializer_content = f'''
from rest_framework import serializers
from {app_label}.models import {model_name}

{nested_serializers}

class {model_name}Serializer(serializers.ModelSerializer):
{nested_fields_code if nested_fields_code else ""}
    class Meta:
        model = {model_name}
        fields = '__all__'
'''
                with open(os.path.join(serializer_dir, f'{model_name.lower()}_serializer.py'), 'w') as f:
                    f.write(serializer_content)

        self.stdout.write(self.style.SUCCESS('Successfully generated serializers'))
