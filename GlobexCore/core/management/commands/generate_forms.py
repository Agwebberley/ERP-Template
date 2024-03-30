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
            inline_formsets = []  # Create an empty list to store the inline formsets

            for model in models:
                model_name = model.__name__
                form_class_name = f'{model_name}Form'

                # Check for related models and prepare to generate inline formsets
                related_models = model._meta.get_fields()

                for related_model in related_models:
                    if related_model.one_to_many or related_model.one_to_one:
                        if related_model.related_model._meta.app_label == app_name:  # Only generate formsets for models within the same app
                            inline_formset_name = f'{model_name}{related_model.name.capitalize()}FormSet'
                            inline_formset_definition = f'class {inline_formset_name}(forms.BaseInlineFormSet):\n\tmodel = {related_model.related_model.__name__}\n\tfields = "__all__"\n\textra = 1\n\n'
                            formset_definitions += inline_formset_definition
                            inline_formsets.append(inline_formset_name)

                form_class_definition = f'class {form_class_name}(MasterDetailForm):\n\tclass Meta:\n\t\tmodel = {model_name}\n\t\tfields = "__all__"\n\n{"".join([f"{related_model.related_model.__name__} = forms.inlineformset_factory({model_name}, {related_model.related_model.__name__}, form={inline_formset_name}, extra=1, fields='__all__')\n" for related_model, inline_formset_name in zip(related_models, inline_formsets)])}'

                f.write(formset_definitions)  # Write formset definitions first
                f.write(form_class_definition)  # Then write form class definitions
