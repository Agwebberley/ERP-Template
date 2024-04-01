from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
from core.models import ModelMeta, FieldMeta
import os

IGNORED_APPS = settings.IGNORED_APPS

class Command(BaseCommand):
    help = 'Generates meta information for the specified app'

    def add_arguments(self, parser):
        parser.add_argument('app', nargs='?', default="*", type=str, help="App label of the application to auto-generate meta information for")

    def handle(self, **options):
        app_name = options['app']
        if app_name == '*':
            app_configs = apps.get_app_configs()
            app_configs = [app for app in app_configs if app.label not in IGNORED_APPS]
        else:
            app_configs = [apps.get_app_config(app_name)]
        
        for app_config in app_configs:
            models = app_config.get_models()
            self.generate_meta(models, app_config.label)
    
    def generate_meta(self, models, app_label):
        for model in models:
            model_name = model.__name__
            model_meta, created = ModelMeta.objects.get_or_create(model_name=f"{app_label}.{model_name}")
            if not created:
                continue
            model_meta.model_verbose_name = model._meta.verbose_name
            model_meta.model_verbose_name_plural = model._meta.verbose_name_plural
            model_meta.model_icon = 'fa fa-cube'
            model_meta.save()
            print(f"Meta information for {model_meta.model_name} created successfully")
            
            for field in model._meta.get_fields():
                """
                field_name = models.CharField(max_length=255)
                field_verbose_name = models.CharField(max_length=255)
                form_hidden = models.BooleanField(default=False)
                list_hidden = models.BooleanField(default=False)
                field_type = models.CharField(max_length=255)
                field_default = models.CharField(max_length=255)
                model = models.ForeignKey(ModelMeta, on_delete=models.CASCADE)
                """
                field_meta, created = FieldMeta.objects.get_or_create(field_name=field.name, model=model_meta)
                if not created:
                    continue
                # If the relationship is ManyToOneRel, verbose_name is not available
                if hasattr(field, 'verbose_name'):
                    field_meta.field_verbose_name = field.verbose_name
                    field_meta.field_default = field.default
                else:
                    field_meta.field_verbose_name = field.name
                field_meta.form_hidden = False
                field_meta.list_hidden = False
                field_meta.field_type = field.get_internal_type()
                field_meta.save()
                print(f"Meta information for {field_meta.field_name} created successfully")
