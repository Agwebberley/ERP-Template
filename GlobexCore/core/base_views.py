from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect

class BaseFormWithInlineFormsetView(CreateView, UpdateView):
    model = None  # This should be overridden in the subclass
    form_class = None  # This should be overridden in the subclass
    inline_formset_classes = []  # List of inline formset classes
    template_name = 'your_generic_template.html'
    success_url = reverse_lazy('your_default_success_url')  # Override this in subclasses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = self.form_class(self.request.POST, instance=self.object)
            context['inline_formsets'] = [
                formset_class(self.request.POST, instance=self.object) for formset_class in self.inline_formset_classes
            ]
        else:
            context['form'] = self.form_class(instance=self.object)
            context['inline_formsets'] = [
                formset_class(instance=self.object) for formset_class in self.inline_formset_classes
            ]
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        context = self.get_context_data()
        inline_formsets = context['inline_formsets']

        if all(formset.is_valid() for formset in inline_formsets):
            for formset in inline_formsets:
                formset.save()
            return response
        else:
            return self.form_invalid(form)
