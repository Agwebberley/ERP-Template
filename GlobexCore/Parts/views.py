from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from core.base_views import MasterCreateView, MasterUpdateView, MasterDeleteView, MasterListView

class partsCreateView(MasterCreateView):
    model = parts
    form_class = partsForm
    success_url = reverse_lazy('')

class partsUpdateView(MasterUpdateView):
    model = parts
    form_class = partsForm
    success_url = reverse_lazy('')

class partsListView(MasterListView):
    model = parts

class partsDeleteView(MasterDeleteView):
    model = parts
    success_url = reverse_lazy('')
