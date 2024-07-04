from django.shortcuts import render
from django.urls import reverse_lazy
from core.base_views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView, BaseDetailView
from .models import Customer
# Create your views here.

class CustomerListView(BaseListView):
    model = Customer

class CustomerCreateView(BaseCreateView):
    model = Customer
    success_url = reverse_lazy('customer-list')


class CustomerUpdateView(BaseUpdateView):
    model = Customer
    success_url = reverse_lazy('customer-list')

class CustomerDeleteView(BaseDeleteView):
    model = Customer
    success_url = reverse_lazy('customer-list')

class CustomerDetailView(BaseDetailView):
    model = Customer