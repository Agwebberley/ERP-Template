from .views import supplierListView, supplierView, supplierDeleteView
from django.urls import path
app_name = 'Suppliers'
urlpatterns = [

path('suppliers/', supplierListView.as_view(), name='supplier_list'),
path('supplier/create/', supplierView.as_view(), name='supplier_create'),
path('supplier/<int:pk>/update/', supplierView.as_view(), name='supplier_update'),
path('supplier/<int:pk>/delete/', supplierDeleteView.as_view(), name='supplier_delete'),
]