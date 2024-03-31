from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from core.base_views import MasterCreateView, MasterUpdateView, MasterDeleteView, MasterListView

class CustomerCreateView(MasterCreateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('')

class CustomerUpdateView(MasterUpdateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('')

class CustomerListView(MasterListView):
    model = Customer

class CustomerDeleteView(MasterDeleteView):
    model = Customer
    success_url = reverse_lazy('')
