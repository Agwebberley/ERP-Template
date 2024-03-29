from .views import inventoryListView, inventoryView, inventoryDeleteView
from django.urls import path
app_name = 'Inventory'
patterns = [

path('inventorys/', InventoryListView.as_view(), name='inventory_list'),
path('inventory/create/', InventoryView.as_view(), name='inventory_create'),
path('inventory/<int:pk>/update/', InventoryView.as_view(), name='inventory_update'),
path('inventory/<int:pk>/delete/', InventoryDeleteView.as_view(), name='inventory_delete'),
]