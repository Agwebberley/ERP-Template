from .views import CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView
from django.urls import path
app_name = 'Customers'
urlpatterns = [

path('customers/', CustomerListView.as_view(), name='customer_list'),
path('customer/create/', CustomerCreateView.as_view(), name='customer_create'),
path('customer/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer_update'),
path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
]