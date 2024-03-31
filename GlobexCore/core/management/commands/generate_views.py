from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
import os

IGNORED_APPS = settings.IGNORED_APPS

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

class Command(BaseCommand):
    help = 'Generates view classes for models in the specified app'

    def add_arguments(self, parser):
        parser.add_argument('app', nargs='?', default="*", type=str, help="App label of the application to auto-generate views for")

    def handle(self, **options):
        app_name = options['app']
        if app_name == '*':
            app_configs = apps.get_app_configs()
            app_configs = [app for app in app_configs if app.label not in IGNORED_APPS]
        else:
            app_configs = [apps.get_app_config(app_name)]
        
        for app_config in app_configs:
            models = app_config.get_models()
            self.generate_views(models, app_config.label)
    
    def generate_views(self, models, app_label):
        views_content = ""
        views_content += f"from django.shortcuts import render, redirect\nfrom django.urls import reverse_lazy\nfrom .forms import *\nfrom core.base_views import MasterCreateView, MasterUpdateView, MasterDeleteView, MasterListView\n"
        for model in models:
            views_content += self.generate_view_for_model(model, app_label)
        
        # Define where and how you want to save the generated view code
        views_directory = os.path.join(settings.BASE_DIR, app_label)
        with open(os.path.join(views_directory, 'views.py'), 'w') as f:
            f.write(views_content)
    
    def generate_view_for_model(self, model, app_label):
        model_name = model.__name__
        form_class_name = f'{model_name}Form'  # Assuming a naming convention for form classes
        success_url = ''  # Define how you want to set the success URL

        # Based on the MasterFormView class from base_views.py
        view_template = f"""
class {model_name}CreateView(MasterCreateView):
    model = {model_name}
    form_class = {form_class_name}
    success_url = reverse_lazy('{success_url}')

class {model_name}UpdateView(MasterUpdateView):
    model = {model_name}
    form_class = {form_class_name}
    success_url = reverse_lazy('{success_url}')

class {model_name}ListView(MasterListView):
    model = {model_name}

class {model_name}DeleteView(MasterDeleteView):
    model = {model_name}
    success_url = reverse_lazy('{success_url}')
"""
        return view_template
