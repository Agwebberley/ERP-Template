from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from core.base_views import MasterFormView, MasterDeleteView, MasterListView

# Index view
def index(request):
    return render(request, 'index.html')