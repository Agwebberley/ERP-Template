from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from core.base_views import MasterCreateView, MasterUpdateView, MasterDeleteView, MasterListView

class inventoryCreateView(MasterCreateView):
    model = inventory
    form_class = inventoryForm
    success_url = reverse_lazy('')

class inventoryUpdateView(MasterUpdateView):
    model = inventory
    form_class = inventoryForm
    success_url = reverse_lazy('')

class inventoryListView(MasterListView):
    model = inventory

class inventoryDeleteView(MasterDeleteView):
    model = inventory
    success_url = reverse_lazy('')
