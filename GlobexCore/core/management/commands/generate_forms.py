import os
from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings

IGNORED_APPS = ['admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles', 'sites', 'auth', 'users', 'groups', 'permissions', 'logentry', 'contenttype', 'session', 'message', 'staticfile', 'site']

class Command(BaseCommand):
    help = 'Generates form classes with inline formsets for each model in the specified app'

    def add_arguments(self, parser):
        parser.add_argument('app', type=str, nargs='?', default='*', help='The app name to generate forms for. Use "*" to generate forms for all apps.')

    def handle(self, **options):
        app_name = options['app']
        if app_name == '*':
            app_configs = apps.get_app_configs()
            app_configs = [app for app in app_configs if app.label not in IGNORED_APPS]
        else:
            app_configs = [apps.get_app_config(app_name)]
        
        for app_config in app_configs:
            models = app_config.get_models()
            self.generate_forms(models, app_config.label)

    def generate_forms(self, models, app_name):
        forms_directory = os.path.join(settings.BASE_DIR, app_name)
        os.makedirs(forms_directory, exist_ok=True)

        with open(os.path.join(forms_directory, 'forms.py'), 'w') as f:
            f.write("from django import forms\nfrom core.base_forms import MasterDetailForm\nfrom .models import *\n\n")

            formset_definitions = ""  # Move the declaration of formset_definitions outside of the for loop
            for model in models:
                model_name = model.__name__
                form_class_name = f'{model_name}Form'

                # Check for related models and prepare to generate inline formsets
                related_models = [rel.related_model for rel in model._meta.related_objects]
                for rel_model in related_models:
                    rel_model_name = rel_model.__name__
                    try:
                        fk_name = rel_model._meta.get_field(rel_model._meta.auto_created).name
                    except Exception:
                        fk_name = None
                    if fk_name:
                        formset_definitions += f"""
{rel_model_name}Formset = MasterDetailForm.get_inline_formset(
    related_model={rel_model_name},
    form={rel_model_name}Form,
    fk_name='{fk_name}',
    extra=1, can_delete=True)\n"""

                # Generate the form class, including formset definitions if any
                form_class_code = f"""class {form_class_name}(MasterDetailForm):
    class Meta(MasterDetailForm.Meta):
        model = {model_name}
        fields = '__all__'
{formset_definitions}\n\n"""
                f.write(form_class_code)
