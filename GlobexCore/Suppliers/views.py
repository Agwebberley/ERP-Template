from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from core.base_views import MasterFormView, MasterDeleteView, MasterListView

class supplierView(MasterFormView):
    model = supplier
    form_class = supplierForm
    success_url = reverse_lazy('/')

class supplierListView(MasterListView):
    model = supplier

class supplierDeleteView(MasterDeleteView):
    model = supplier
    success_url = reverse_lazy('/')
