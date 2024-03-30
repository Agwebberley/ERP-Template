from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    # index.html
    path('', views.index, name='index'),
]