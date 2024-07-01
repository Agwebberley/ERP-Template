from django.urls import path
from .base_views import home

urlpatterns = [
    path('', home, name='home'),
]