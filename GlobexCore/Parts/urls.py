from .views import partsListView, partsView, partsDeleteView
from django.urls import path
app_name = 'Parts'
patterns = [

path('partss/', partsListView.as_view(), name='parts_list'),
path('parts/create/', partsView.as_view(), name='parts_create'),
path('parts/<int:pk>/update/', partsView.as_view(), name='parts_update'),
path('parts/<int:pk>/delete/', partsDeleteView.as_view(), name='parts_delete'),
]