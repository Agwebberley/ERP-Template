from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
import os

IGNORED_APPS = ['admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles', 'sites', 'auth', 'users', 'groups', 'permissions', 'logentry', 'contenttype', 'session', 'message', 'staticfile', 'site']

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
        views_content += f"from django.views.generic import View\nfrom django.shortcuts import render, redirect\nfrom .forms import *\n\n"
        for model in models:
            views_content += self.generate_view_for_model(model, app_label)
        
        # Define where and how you want to save the generated view code
        views_directory = os.path.join(settings.BASE_DIR, app_label)
        with open(os.path.join(views_directory, 'views.py'), 'w') as f:
            f.write(views_content)
    
    def generate_view_for_model(self, model, app_label):
        model_name = model.__name__
        form_class_name = f'{model_name}Form'  # Assuming a naming convention for form classes
        view_class_name = f'{model_name}View'
        success_url = '/'  # Define how you want to set the success URL

        view_template = f"""
class {view_class_name}(View):
    template_name = 'form.html'
    form_class = {form_class_name}
    success_url = '{success_url}'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        inline_formsets = form.get_inline_formsets()
        return render(request, self.template_name, {{'form': form, 'inline_formsets': inline_formsets}})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            main_instance = form.save()
            inline_formsets = form.get_inline_formsets(instance=main_instance, data=request.POST, files=request.FILES)
            if all(formset.is_valid() for formset in inline_formsets):
                for formset in inline_formsets:
                    formset.save()
                return redirect(self.success_url)
        inline_formsets = form.get_inline_formsets(data=request.POST, files=request.FILES)
        return render(request, self.template_name, {{'form': form, 'inline_formsets': inline_formsets}})
"""

        return view_template
