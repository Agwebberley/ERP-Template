from django.urls import Resolver404, resolve, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from core.models import ModelPermissions

from django.shortcuts import render, redirect

# Becuase the Navigation bar is used in multiple views, we can create a mixin for it
class NavigationMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models'] = {}
        for model in ModelPermissions.objects.all():
            model_app, model_name = model.model_name.split('.')
            model_permissions = model.can_read
            model_url = f'{model_app}:{model_name.lower()}_list'
            if model_permissions:
                if model_app not in context['models']:
                    context['models'][model_app] = []
                context['models'][model_app].append((model_name, model_url))
        return context

class MasterCreateView(NavigationMixin, CreateView):
    model = None  # This should be overridden in the subclass
    form_class = None  # This should be overridden in the subclass
    inline_formset_classes = []  # List of inline formset classes
    template_name = 'form.html'
    success_url = reverse_lazy('/')  # Override this in subclasses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the inline formsets to the context
        form = self.form_class()
        inline_formsets = form.get_inline_formsets()
        context['inline_formsets'] = inline_formsets
        print(context)
        return context


class MasterUpdateView(NavigationMixin, UpdateView):
    model = None  # This should be overridden in the subclass
    form_class = None  # This should be overridden in the subclass
    inline_formset_classes = []  # List of inline formset classes
    template_name = 'form.html'
    success_url = reverse_lazy('/')  # Override this in subclasses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        instance = self.model.objects.get(pk=kwargs['pk'])
        form = self.form_class(instance=instance)
        inline_formsets = form.get_inline_formsets(instance=instance)
        return render(request, 'detail_or_update_template.html', {'form': form, 'inline_formsets': inline_formsets})

    def post(self, request, *args, **kwargs):
        instance = self.model.objects.get(pk=kwargs['pk'])
        form = self.form_class(data=request.POST, files=request.FILES, instance=instance)

        if form.is_valid():
            main_instance = form.save()
            inline_formsets = form.get_inline_formsets(instance=main_instance, data=request.POST, files=request.FILES)
            if all(formset.is_valid() for formset in inline_formsets):
                for formset in inline_formsets:
                    formset.save()
                return redirect(self.success_url)

        inline_formsets = form.get_inline_formsets(data=request.POST, files=request.FILES, instance=instance)
        return render(request, 'detail_or_update_template.html', {'form': form, 'inline_formsets': inline_formsets})

class MasterListView(NavigationMixin, ListView):
    model = None  # This should be overridden in the subclass
    template_name = 'listview.html'  # Specify your read template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_fields'] = [field.name for field in self.model._meta.get_fields()]
        context['patterns'] = {'Update': f'{self.model.__name__.lower()}_update', 'Delete': f'{self.model.__name__.lower()}_delete'}
        context['h1'] = self.model.__name__ + 's'
        context['bpattern'] = f'{self.model._meta.app_label}:{self.model.__name__.lower()}_create'
        context['bname'] = f'Create {self.model.__name__}'
        return context

class MasterDeleteView(DeleteView, NavigationMixin):
    model = None # This should be overridden in the subclass
    template_name = 'delete.html'  # Confirmation template
    success_url = reverse_lazy('/')  # Override this in subclasses

    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['object_name'] = str(object)
        context['pattern'] = f'{self.model.__name__.lower()}_list'
        return context
