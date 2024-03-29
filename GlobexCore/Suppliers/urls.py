from .views import supplierListView, supplierView, supplierDeleteView
from django.urls import path
app_name = 'Suppliers'
patterns = [

path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
path('supplier/create/', SupplierView.as_view(), name='supplier_create'),
path('supplier/<int:pk>/update/', SupplierView.as_view(), name='supplier_update'),
path('supplier/<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier_delete'),
]