from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.apps import apps
from .models import ModelConfiguration
from .utils import get_enabled_fields, generate_dynamic_form, get_actions

class BaseCreateView(CreateView):
    template_name = 'form.html'

    def get_form_class(self):
        # Dynamically get the form class based on the model
        model_config = get_object_or_404(ModelConfiguration, model_name=self.model.__name__)
        absolute_url = reverse_lazy(model_config.model_name.lower() + '-list')
        return generate_dynamic_form(model_config.app.name, model_config.model_name, self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_config = get_object_or_404(ModelConfiguration, model_name=self.model.__name__)
        context['config'] = model_config
        context['enabled_fields'] = get_enabled_fields(model_config.app.name, model_config.model_name, self.request.user)
        context['return_url'] = model_config.model_name.lower() + '-list'
        return context


class BaseUpdateView(UpdateView):
    template_name = 'form.html'

    def get_form_class(self):
        # Dynamically get the form class based on the model
        model_config = get_object_or_404(ModelConfiguration, model_name=self.model.__name__)
        return generate_dynamic_form(model_config.app.name, model_config.model_name, self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_config = get_object_or_404(ModelConfiguration, model_name=self.model.__name__)
        context['config'] = model_config
        context['enabled_fields'] = get_enabled_fields(model_config.app.name, model_config.model_name, self.request.user)
        context['return_url'] = model_config.model_name.lower() + '-list'
        return context

class BaseListView(ListView):
    template_name = 'list.html'

    def get_queryset(self):
        model_config = get_object_or_404(ModelConfiguration, model_name=self.model.__name__)
        queryset = self.model.objects.all()
        if model_config.default_sort_by:
            queryset = queryset.order_by(model_config.default_sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_config = get_object_or_404(ModelConfiguration, model_name=self.model.__name__)
        context['config'] = model_config
        context['enabled_fields'] = get_enabled_fields(model_config.app.name, model_config.model_name, self.request.user, view_type='list')
        context['actions'] = get_actions(model_config.app.name, model_config.model_name)
        return context

class BaseDetailView(DetailView):
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_config = get_object_or_404(ModelConfiguration, model_name=self.model.__name__)
        context['config'] = model_config
        context['enabled_fields'] = get_enabled_fields(model_config.app.name, model_config.model_name, self.request.user, view_type='show')
        context['return_url'] = model_config.model_name.lower() + '-list'
        context['edit_url'] = model_config.model_name.lower() + '-update'
        context['delete_url'] = model_config.model_name.lower() + '-delete'

        return context

class BaseDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_url'] = self.model.__name__.lower() + '-list'
        return context

class BaseMasterDetailView(DetailView):
    template_name = 'base_master_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_config = get_object_or_404(ModelConfiguration, model_name=self.model.__name__)
        context['config'] = model_config
        context['enabled_fields'] = get_enabled_fields(model_config.app.name, model_config.model_name, self.request.user, view_type='show')
        
        # Handle related models and tabs
        context['related_models'] = []
        for related_model_name in model_config.related_models:
            related_model_class = apps.get_model(app_label=model_config.app.name, model_name=related_model_name)
            related_objects = related_model_class.objects.filter(**{f"{self.model.__name__.lower()}_id": self.object.id})
            context['related_models'].append({
                'name': related_model_name,
                'objects': related_objects,
                'fields': get_enabled_fields(model_config.app.name, related_model_name, self.request.user, view_type='list')
            })

        return context

def home(request):
    return render(request, 'home.html')