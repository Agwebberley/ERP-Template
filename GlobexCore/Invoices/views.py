from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from core.base_views import MasterFormView, MasterDeleteView, MasterListView

class invoiceDetailsView(MasterFormView):
    model = invoiceDetails
    form_class = invoiceDetailsForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formsets = context['form'].formsets
        inlineformset_verbose_names = [formset.verbose_name_plural.title() for formset in formsets]
        context['inlineformset_verbose_names'] = inlineformset_verbose_names
        return context
    success_url = reverse_lazy('')

class invoiceDetailsListView(MasterListView):
    model = invoiceDetails

class invoiceDetailsDeleteView(MasterDeleteView):
    model = invoiceDetails
    success_url = reverse_lazy('')

class invoiceHeadersView(MasterFormView):
    model = invoiceHeaders
    form_class = invoiceHeadersForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formsets = context['form'].formsets
        inlineformset_verbose_names = [formset.verbose_name_plural.title() for formset in formsets]
        context['inlineformset_verbose_names'] = inlineformset_verbose_names
        return context
    success_url = reverse_lazy('')

class invoiceHeadersListView(MasterListView):
    model = invoiceHeaders

class invoiceHeadersDeleteView(MasterDeleteView):
    model = invoiceHeaders
    success_url = reverse_lazy('')
