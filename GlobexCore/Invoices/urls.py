from .views import invoiceDetailsListView, invoiceDetailsView, invoiceDetailsDeleteView
from .views import invoiceHeadersListView, invoiceHeadersView, invoiceHeadersDeleteView
from django.urls import path
app_name = 'Invoices'
patterns = [

path('invoicedetailss/', InvoicedetailsListView.as_view(), name='invoicedetails_list'),
path('invoicedetails/create/', InvoicedetailsView.as_view(), name='invoicedetails_create'),
path('invoicedetails/<int:pk>/update/', InvoicedetailsView.as_view(), name='invoicedetails_update'),
path('invoicedetails/<int:pk>/delete/', InvoicedetailsDeleteView.as_view(), name='invoicedetails_delete'),

path('invoiceheaderss/', InvoiceheadersListView.as_view(), name='invoiceheaders_list'),
path('invoiceheaders/create/', InvoiceheadersView.as_view(), name='invoiceheaders_create'),
path('invoiceheaders/<int:pk>/update/', InvoiceheadersView.as_view(), name='invoiceheaders_update'),
path('invoiceheaders/<int:pk>/delete/', InvoiceheadersDeleteView.as_view(), name='invoiceheaders_delete'),
]