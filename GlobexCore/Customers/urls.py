from .views import CustomerListView, CustomerView, CustomerDeleteView
from django.urls import path
app_name = 'Customers'
patterns = [

path('customers/', CustomerListView.as_view(), name='customer_list'),
path('customer/create/', CustomerView.as_view(), name='customer_create'),
path('customer/<int:pk>/update/', CustomerView.as_view(), name='customer_update'),
path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
]