from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from core.base_views import MasterFormView, MasterDeleteView, MasterListView

class partsView(MasterFormView):
    model = parts
    form_class = partsForm
    success_url = reverse_lazy('/')

class partsListView(MasterListView):
    model = parts

class partsDeleteView(MasterDeleteView):
    model = parts
    success_url = reverse_lazy('/')
