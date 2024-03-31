from .views import partsListView, partsCreateView, partsUpdateView, partsDeleteView
from django.urls import path
app_name = 'Parts'
urlpatterns = [

path('partss/', partsListView.as_view(), name='parts_list'),
path('parts/create/', partsCreateView.as_view(), name='parts_create'),
path('parts/<int:pk>/update/', partsUpdateView.as_view(), name='parts_update'),
path('parts/<int:pk>/delete/', partsDeleteView.as_view(), name='parts_delete'),
]