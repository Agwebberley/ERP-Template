# The purpose of this script is to add any new apps, models, or fields to thier respective tables in the Meta database. This script is run whenever the server is started.

from django.apps import apps
from django.conf import settings
from core.models import Model, Field, App, ModelPermissions
from django.core.management.base import BaseCommand
import os
import json

IGNORED_APPS = settings.IGNORED_APPS

class Command(BaseCommand):
    help = 'Generates meta information for the specified app'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='?', default="*", type=str, help="The name of the file to generate the meta information for. If not specified, all files will be generated.")

    def handle(self, **options):
        file = options['file']
        if file == "*":
            # For every file in the schema folder
            for file in os.listdir("schemas"):
                self.generate_meta("schemas/" + file)
        else:
            # Make sure the file exists
            if os.path.exists(f"schemas/{file}"):
                file = "schemas/" + file
                self.generate_meta(file)
        
    
    def generate_meta(self, models):
        # Check for a json file in the schemas folder

        # Load the json file
        with open(models) as f:
            data = json.load(f)
        
        # Create a model meta object for each model
        for app_name, app in data.items():
            app_obj, created = App.objects.get_or_create(
                app_name=app_name,
                defaults={
                    'app_verbose_name': app_name,
                    'app_icon': "fa fa-table"
                }
            )
            for model_name, model in app.items():
                model_obj, created = Model.objects.get_or_create(
                    model_name=f"{app_name}.{model_name}",
                    defaults={
                        'model_verbose_name': model_name,
                        'model_verbose_name_plural': model_name,
                        'model_icon': "fa fa-table",
                        'app': app_obj
                    }
                )

                # Create a field meta object for each field
                for field in model['columns']:
                    field_name, field_info = list(field.items())[0]
                    field_obj, _ = Field.objects.get_or_create(
                        model=model_obj,
                        field_name=field_name,
                        defaults={
                            'field_verbose_name': field_name,
                            'form_hidden': False,
                            'list_hidden': False,
                            'field_type': field_info[0],
                            'model': model_obj
                        }
                   )
        print("Meta information generated successfully")