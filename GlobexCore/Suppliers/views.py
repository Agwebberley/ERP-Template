from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from core.base_views import MasterFormView, MasterDeleteView, MasterListView

class supplierView(MasterFormView):
    model = supplier
    form_class = supplierForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formsets = context['form'].formsets
        inlineformset_verbose_names = [formset.verbose_name_plural.title() for formset in formsets]
        context['inlineformset_verbose_names'] = inlineformset_verbose_names
        return context
    success_url = reverse_lazy('')

class supplierListView(MasterListView):
    model = supplier

class supplierDeleteView(MasterDeleteView):
    model = supplier
    success_url = reverse_lazy('')
