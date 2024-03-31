from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from core.base_views import MasterCreateView, MasterUpdateView, MasterDeleteView, MasterListView

class orderDetailsCreateView(MasterCreateView):
    model = orderDetails
    form_class = orderDetailsForm
    success_url = reverse_lazy('')

class orderDetailsUpdateView(MasterUpdateView):
    model = orderDetails
    form_class = orderDetailsForm
    success_url = reverse_lazy('')

class orderDetailsListView(MasterListView):
    model = orderDetails

class orderDetailsDeleteView(MasterDeleteView):
    model = orderDetails
    success_url = reverse_lazy('')

class orderHeadersCreateView(MasterCreateView):
    model = orderHeaders
    form_class = orderHeadersForm
    success_url = reverse_lazy('')

class orderHeadersUpdateView(MasterUpdateView):
    model = orderHeaders
    form_class = orderHeadersForm
    success_url = reverse_lazy('')

class orderHeadersListView(MasterListView):
    model = orderHeaders

class orderHeadersDeleteView(MasterDeleteView):
    model = orderHeaders
    success_url = reverse_lazy('')
