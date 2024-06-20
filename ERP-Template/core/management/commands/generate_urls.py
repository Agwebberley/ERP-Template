from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Generate URLs for each model in each app'

    def handle(self, *args, **kwargs):
        app_configs = apps.get_app_configs()
        urls_content = '''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
'''

        for app_config in app_configs:
            app_label = app_config.label
            # Check if in INGORED_APPS
            if app_label in getattr(settings, 'IGNORED_APPS', []):
                continue
            app_models = app_config.get_models()
            for model in app_models:
                model_name = model.__name__
                urls_content += f'from {app_label}.views.{model_name.lower()}_viewset import {model_name}ViewSet\n'

        urls_content += '\nrouter = DefaultRouter()\n'

        for app_config in app_configs:
            app_label = app_config.label
            # Check if in INGORED_APPS
            if app_label in getattr(settings, 'IGNORED_APPS', []):
                continue
            app_models = app_config.get_models()
            for model in app_models:
                model_name = model.__name__
                urls_content += f'router.register(r\'{model_name.lower()}\', {model_name}ViewSet)\n'

        urls_content += '''
urlpatterns = [
    path('', include(router.urls)),
]
'''

        with open('generated_urls.py', 'w') as f:
            f.write(urls_content)

        self.stdout.write(self.style.SUCCESS('Successfully generated URLs'))
