from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from core.models import ModelPermissions
# Index view
def index(request):
    context = {}  # Define the context variable
    context['models'] = {}  # Initialize the models dictionary
    for model in ModelPermissions.objects.all():  # Fix the indentation
        model_app, model_name = model.model_name.split('.')
        model_permissions = model.can_read
        model_url = f'{model_app}:{model_name.lower()}_list'
        # Check if the url is valid
        if model_permissions:
            if model_app not in context['models']:
                context['models'][model_app] = []
            context['models'][model_app].append((model_name, model_url))
    return render(request, 'home/index.html', context)