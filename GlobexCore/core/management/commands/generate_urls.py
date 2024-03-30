from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
import os

IGNORED_APPS = ['admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles', 'sites', 'auth', 'users', 'groups', 'permissions', 'logentry', 'contenttype', 'session', 'message', 'staticfile', 'site']

class Command(BaseCommand):
    help = 'Generates urls.py for the specified app'

    def add_arguments(self, parser):
        parser.add_argument('app', nargs='?', default="*", type=str, help="App label of the application to auto-generate urls for")

    def handle(self, **options):
        app_name = options['app']
        if app_name == '*':
            app_configs = apps.get_app_configs()
            app_configs = [app for app in app_configs if app.label not in IGNORED_APPS]
        else:
            app_configs = [apps.get_app_config(app_name)]
        
        for app_config in app_configs:
            models = app_config.get_models()
            self.generate_urls(models, app_config.label)

    def generate_urls(self, models, app_label):
        urls_content = ""
        imports = ""
        models_list = list(models)  # Convert models to a list
        for model in models_list:
            model_name = model.__name__
            imports += f"from .views import {model_name}ListView, {model_name}View, {model_name}DeleteView\n"
        urls_content += imports
        urls_content += "from django.urls import path\napp_name = '" + app_label + "'\nurlpatterns = [\n"
        patterns = ""
        for model in models_list:
            model_name = model.__name__.lower()
            model_name_n = model.__name__
            model_name_plural = model_name + 's'
            patterns += f"""
path('{model_name_plural}/', {model_name_n}ListView.as_view(), name='{model_name}_list'),
path('{model_name}/create/', {model_name_n}View.as_view(), name='{model_name}_create'),
path('{model_name}/<int:pk>/update/', {model_name_n}View.as_view(), name='{model_name}_update'),
path('{model_name}/<int:pk>/delete/', {model_name_n}DeleteView.as_view(), name='{model_name}_delete'),
"""
        urls_content += patterns
        urls_content += "]"
        
        # Define where and how you want to save the generated URL code
        urls_directory = os.path.join(settings.BASE_DIR, app_label)
        with open(os.path.join(urls_directory, 'urls.py'), 'w') as f:
            f.write(urls_content)
        
        # Register the generated URLs in the main urls.py file
        urls_file = os.path.join(settings.BASE_DIR, settings.ROOT_URLCONF.split('.')[0], 'urls.py')
        print(urls_file)
        with open(urls_file, 'r') as f:
            content = f.read()
        if app_label not in content:
            with open(urls_file, 'a') as f:
                f.write(f"\nurlpatterns.append(path('{app_label}/', include('{app_label}.urls')))")

        print("URLs generated successfully!")