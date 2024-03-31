from .views import supplierListView, supplierCreateView, supplierUpdateView, supplierDeleteView
from django.urls import path
app_name = 'Suppliers'
urlpatterns = [

path('suppliers/', supplierListView.as_view(), name='supplier_list'),
path('supplier/create/', supplierCreateView.as_view(), name='supplier_create'),
path('supplier/<int:pk>/update/', supplierUpdateView.as_view(), name='supplier_update'),
path('supplier/<int:pk>/delete/', supplierDeleteView.as_view(), name='supplier_delete'),
]