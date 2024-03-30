from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from core.base_views import MasterFormView, MasterDeleteView, MasterListView

class orderDetailsView(MasterFormView):
    model = orderDetails
    form_class = orderDetailsForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formsets = context['form'].formsets
        inlineformset_verbose_names = [formset.verbose_name_plural.title() for formset in formsets]
        context['inlineformset_verbose_names'] = inlineformset_verbose_names
        return context
    success_url = reverse_lazy('')

class orderDetailsListView(MasterListView):
    model = orderDetails

class orderDetailsDeleteView(MasterDeleteView):
    model = orderDetails
    success_url = reverse_lazy('')

class orderHeadersView(MasterFormView):
    model = orderHeaders
    form_class = orderHeadersForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formsets = context['form'].formsets
        inlineformset_verbose_names = [formset.verbose_name_plural.title() for formset in formsets]
        context['inlineformset_verbose_names'] = inlineformset_verbose_names
        return context
    success_url = reverse_lazy('')

class orderHeadersListView(MasterListView):
    model = orderHeaders

class orderHeadersDeleteView(MasterDeleteView):
    model = orderHeaders
    success_url = reverse_lazy('')
