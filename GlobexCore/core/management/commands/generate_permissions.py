from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
from core.models import ModelPermissions
import os


IGNORED_APPS = ['admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles', 'sites', 'auth', 'users', 'groups', 'permissions', 'logentry', 'contenttype', 'session', 'message', 'staticfile', 'site']

# For each model, generate a permission for each CRUD operation
class Command(BaseCommand):
    help = 'Generates permissions for the specified app'

    def add_arguments(self, parser):
        parser.add_argument('app', nargs='?', default="*", type=str, help="App label of the application to auto-generate permissions for")

    def handle(self, **options):
        app_name = options['app']
        if app_name == '*':
            app_configs = apps.get_app_configs()
            app_configs = [app for app in app_configs if app.label not in IGNORED_APPS]
        else:
            app_configs = [apps.get_app_config(app_name)]
        
        for app_config in app_configs:
            models = app_config.get_models()
            self.generate_permissions(models, app_config.label)
        
        # Remove permissions for models that no longer exist
        all_models = apps.get_models()
        all_models = [f"{model._meta.app_label}.{model.__name__}" for model in all_models]
        self.remove_permissions(all_models)


    def generate_permissions(self, models, app_label):
        for model in models:
            model_name = app_label + "." + model.__name__
            ModelPermissions.objects.get_or_create(model_name=model_name)
            print(f"Permissions for {model_name} created successfully")
    
    def remove_permissions(self, models):
        # Remove permissions for models that no longer exist
        for permission in ModelPermissions.objects.all():
            if permission.model_name not in models:
                permission.delete()
                print(f"Permissions for {permission.model_name} deleted successfully")