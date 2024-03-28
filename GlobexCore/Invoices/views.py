from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from core.base_views import MasterFormView, MasterDeleteView, MasterListView

class invoiceDetailsView(MasterFormView):
    model = invoiceDetails
    form_class = invoiceDetailsForm
    success_url = reverse_lazy('/')

class invoiceDetailsListView(MasterListView):
    model = invoiceDetails

class invoiceDetailsDeleteView(MasterDeleteView):
    model = invoiceDetails
    success_url = reverse_lazy('/')

class invoiceHeadersView(MasterFormView):
    model = invoiceHeaders
    form_class = invoiceHeadersForm
    success_url = reverse_lazy('/')

class invoiceHeadersListView(MasterListView):
    model = invoiceHeaders

class invoiceHeadersDeleteView(MasterDeleteView):
    model = invoiceHeaders
    success_url = reverse_lazy('/')
