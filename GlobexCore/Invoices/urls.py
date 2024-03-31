from .views import invoiceDetailsListView, invoiceDetailsCreateView, invoiceDetailsUpdateView, invoiceDetailsDeleteView
from .views import invoiceHeadersListView, invoiceHeadersCreateView, invoiceHeadersUpdateView, invoiceHeadersDeleteView
from django.urls import path
app_name = 'Invoices'
urlpatterns = [

path('invoicedetailss/', invoiceDetailsListView.as_view(), name='invoicedetails_list'),
path('invoicedetails/create/', invoiceDetailsCreateView.as_view(), name='invoicedetails_create'),
path('invoicedetails/<int:pk>/update/', invoiceDetailsUpdateView.as_view(), name='invoicedetails_update'),
path('invoicedetails/<int:pk>/delete/', invoiceDetailsDeleteView.as_view(), name='invoicedetails_delete'),

path('invoiceheaderss/', invoiceHeadersListView.as_view(), name='invoiceheaders_list'),
path('invoiceheaders/create/', invoiceHeadersCreateView.as_view(), name='invoiceheaders_create'),
path('invoiceheaders/<int:pk>/update/', invoiceHeadersUpdateView.as_view(), name='invoiceheaders_update'),
path('invoiceheaders/<int:pk>/delete/', invoiceHeadersDeleteView.as_view(), name='invoiceheaders_delete'),
]