from .views import invoiceDetailsListView, invoiceDetailsView, invoiceDetailsDeleteView
from .views import invoiceHeadersListView, invoiceHeadersView, invoiceHeadersDeleteView
from django.urls import path
app_name = 'Invoices'
patterns = [

path('invoicedetailss/', invoiceDetailsListView.as_view(), name='invoicedetails_list'),
path('invoicedetails/create/', invoiceDetailsView.as_view(), name='invoicedetails_create'),
path('invoicedetails/<int:pk>/update/', invoiceDetailsView.as_view(), name='invoicedetails_update'),
path('invoicedetails/<int:pk>/delete/', invoiceDetailsDeleteView.as_view(), name='invoicedetails_delete'),

path('invoiceheaderss/', invoiceHeadersListView.as_view(), name='invoiceheaders_list'),
path('invoiceheaders/create/', invoiceHeadersView.as_view(), name='invoiceheaders_create'),
path('invoiceheaders/<int:pk>/update/', invoiceHeadersView.as_view(), name='invoiceheaders_update'),
path('invoiceheaders/<int:pk>/delete/', invoiceHeadersDeleteView.as_view(), name='invoiceheaders_delete'),
]