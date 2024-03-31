from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from core.base_views import MasterCreateView, MasterUpdateView, MasterDeleteView, MasterListView

class invoiceDetailsCreateView(MasterCreateView):
    model = invoiceDetails
    form_class = invoiceDetailsForm
    success_url = reverse_lazy('')

class invoiceDetailsUpdateView(MasterUpdateView):
    model = invoiceDetails
    form_class = invoiceDetailsForm
    success_url = reverse_lazy('')

class invoiceDetailsListView(MasterListView):
    model = invoiceDetails

class invoiceDetailsDeleteView(MasterDeleteView):
    model = invoiceDetails
    success_url = reverse_lazy('')

class invoiceHeadersCreateView(MasterCreateView):
    model = invoiceHeaders
    form_class = invoiceHeadersForm
    success_url = reverse_lazy('')

class invoiceHeadersUpdateView(MasterUpdateView):
    model = invoiceHeaders
    form_class = invoiceHeadersForm
    success_url = reverse_lazy('')

class invoiceHeadersListView(MasterListView):
    model = invoiceHeaders

class invoiceHeadersDeleteView(MasterDeleteView):
    model = invoiceHeaders
    success_url = reverse_lazy('')
