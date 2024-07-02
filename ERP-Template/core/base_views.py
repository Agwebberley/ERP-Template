from django.http import JsonResponse
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.apps import apps
from .models import ModelConfiguration
from .utils import generate_inline_formset, generate_model_form, get_enabled_fields, generate_dynamic_form, get_actions
from django.contrib.auth.views import LoginView, LogoutView

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

class MasterDetailCreateView(CreateView):
    template_name = 'master_detail_form.html'
    
    def get(self, request, app_label, model_name):
        parent_model = apps.get_model(app_label, model_name)
        child_models = [rel.related_model for rel in parent_model._meta.related_objects]

        parent_form_class = generate_model_form(app_label, parent_model.__name__.lower(), self.request.user)
        parent_form = parent_form_class()
        
        child_formsets = []
        for child_model in child_models:
            formset_class = generate_inline_formset(app_label, parent_model, child_model, self.request.user)
            formset = formset_class()
            child_formsets.append((child_model._meta.verbose_name_plural, formset))

        return render(request, self.template_name, {
            'parent_form': parent_form,
            'child_formsets': child_formsets,
            'model_name': model_name,
            'app_label': app_label,
            'return_url': model_name.lower() + '-list'
        })

    def post(self, request, app_label, model_name):
        parent_model = apps.get_model(app_label, model_name)
        child_models = [rel.related_model for rel in parent_model._meta.related_objects]

        parent_form_class = generate_model_form(app_label, parent_model.__name__.lower(), self.request.user)
        parent_form = parent_form_class(request.POST)

        child_formsets = []
        formset_valid = True
        for child_model in child_models:
            formset_class = generate_inline_formset(app_label, parent_model, child_model, self.request.user)
            formset = formset_class(request.POST)
            child_formsets.append((child_model._meta.verbose_name_plural, formset))
            if not formset.is_valid():
                formset_valid = False

        if parent_form.is_valid() and formset_valid:
            parent_instance = parent_form.save()
            for _, formset in child_formsets:
                formset.instance = parent_instance
                formset.save()
            # Use success_url instead of redirect
            return self.success_url

        return render(request, self.template_name, {
            'parent_form': parent_form,
            'child_formsets': child_formsets,
            'model_name': model_name,
            'app_label': app_label,
            'return_url': model_name.lower() + '-list'
        })
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_config = get_object_or_404(ModelConfiguration, model_name=self.model.__name__)
        context['config'] = model_config
        context['enabled_fields'] = get_enabled_fields(model_config.app.name, model_config.model_name, self.request.user, view_type='form')
        context['return_url'] = model_config.model_name.lower() + '-list'
        return context

class MasterDetailUpdateView(UpdateView):
    template_name = 'master_detail_form.html'
    success_url = reverse_lazy('home')

    def get(self, request, app_label, model_name, pk):
        parent_model = apps.get_model(app_label, model_name)
        instance = get_object_or_404(parent_model, pk=pk)
        child_models = [rel.related_model for rel in parent_model._meta.related_objects]

        parent_form_class = generate_model_form(app_label, parent_model.__name__.lower(), self.request.user)
        parent_form = parent_form_class(instance=instance)
        
        child_formsets = []
        for child_model in child_models:
            formset_class = generate_inline_formset(app_label, parent_model, child_model, self.request.user)
            formset = formset_class(instance=instance)
            child_formsets.append((child_model._meta.verbose_name_plural, formset))

        return render(request, self.template_name, {
            'parent_form': parent_form,
            'child_formsets': child_formsets,
            'model_name': model_name,
            'app_label': app_label,
            'return_url': model_name.lower() + '-list'
        })

    def post(self, request, app_label, model_name, pk):
        parent_model = apps.get_model(app_label, model_name)
        instance = get_object_or_404(parent_model, pk=pk)
        child_models = [rel.related_model for rel in parent_model._meta.related_objects]

        parent_form_class = generate_model_form(app_label, model_name, self.request.user)
        parent_form = parent_form_class(request.POST, instance=instance)
        
        child_formsets = []
        formset_valid = True
        for child_model in child_models:
            formset_class = generate_inline_formset(app_label, parent_model, child_model, self.request.user)
            formset = formset_class(request.POST, instance=instance)
            child_formsets.append((child_model._meta.verbose_name_plural, formset))
            if not formset.is_valid():
                formset_valid = False

        if parent_form.is_valid() and formset_valid:
            parent_instance = parent_form.save()
            for _, formset in child_formsets:
                formset.instance = parent_instance
                formset.save()
            # Use success_url instead of redirect
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'parent_form': parent_form,
            'child_formsets': child_formsets,
            'model_name': model_name,
            'app_label': app_label,
            'return_url': model_name.lower() + '-list'
        })
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_config = get_object_or_404(ModelConfiguration, model_name=self.model.__name__)
        context['config'] = model_config
        context['enabled_fields'] = get_enabled_fields(model_config.app.name, model_config.model_name, self.request.user, view_type='form')
        context['return_url'] = model_config.model_name.lower() + '-list'
        return context

def home(request):
    return render(request, 'home.html')

class AddFormsetRowView(View):
    def post(self, request, app_label, model_name):
        parent_model = apps.get_model(app_label, model_name)
        child_model_name = request.POST.get('child_model_name')
        child_model = apps.get_model(app_label, child_model_name)

        formset_class = generate_inline_formset(parent_model, child_model)
        formset = formset_class()

        form_idx = request.POST.get('form_idx')

        new_form = formset.empty_form
        new_form_html = new_form.as_p().replace('__prefix__', str(form_idx))

        return JsonResponse({'form_html': new_form_html})

class LoginView(LoginView):
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        context['saveOveride'] = 'Login'
        context['hOveride'] = 'Login'
        return context

class LogoutView(LogoutView):
    next_page = reverse_lazy('home')
    template_name = 'home.html'
