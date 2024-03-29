from .views import partsListView, partsView, partsDeleteView
from django.urls import path
app_name = 'Parts'
patterns = [

path('partss/', PartsListView.as_view(), name='parts_list'),
path('parts/create/', PartsView.as_view(), name='parts_create'),
path('parts/<int:pk>/update/', PartsView.as_view(), name='parts_update'),
path('parts/<int:pk>/delete/', PartsDeleteView.as_view(), name='parts_delete'),
]