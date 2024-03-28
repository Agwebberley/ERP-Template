from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from core.base_views import MasterFormView, MasterDeleteView, MasterListView

class CustomerView(MasterFormView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('/')

class CustomerListView(MasterListView):
    model = Customer

class CustomerDeleteView(MasterDeleteView):
    model = Customer
    success_url = reverse_lazy('/')
