import os
from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings

IGNORED_APPS = settings.IGNORED_APPS

class Command(BaseCommand):
    help = 'Generates form classes with inline formsets for each model in the specified app'

    def add_arguments(self, parser):
        parser.add_argument('app', type=str, nargs='?', default='*', help='The app name to generate admin forms for. Use "*" to generate forms for all apps.')

    def handle(self, **options):
        app_name = options['app']
        if app_name == '*':
            app_configs = apps.get_app_configs()
            app_configs = [app for app in app_configs if app.label not in IGNORED_APPS]
        else:
            app_configs = [apps.get_app_config(app_name)]
        
        for app_config in app_configs:
            models = app_config.get_models()
            self.generate_admin(models, app_config.label)

    def generate_admin(self, models, app_name):
        admin_directory = os.path.join(settings.BASE_DIR, app_name)
        os.makedirs(admin_directory, exist_ok=True)

        with open(os.path.join(admin_directory, 'admin.py'), 'w') as f:
            f.write("from django.contrib import admin\n")
            f.write("from core.models import App, Model, Field\nfrom .models import *\n\n")

            for model in models:
                model_name = model.__name__
                admin_class_name = f'{model_name}Admin'

                admin_class_definition = f'''
class {admin_class_name}(admin.ModelAdmin):
    model = {model_name}

    @property
    def list_display(self):
        try:
            app = App.objects.get(app_name=self.model._meta.app_label)
            return [field.field_name for field in Field.objects.filter(model=Model.objects.get(model_name=self.model.__name__, app=app)) if not field.list_hidden]
        except Exception:
            return ['__str__']  # Default to '__str__' if an error occurs

admin.site.register({model_name}, {admin_class_name})
'''
                f.write(admin_class_definition)





                