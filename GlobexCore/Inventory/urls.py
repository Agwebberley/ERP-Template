from .views import inventoryListView, inventoryView, inventoryDeleteView
from django.urls import path
app_name = 'Inventory'
patterns = [

path('inventorys/', inventoryListView.as_view(), name='inventory_list'),
path('inventory/create/', inventoryView.as_view(), name='inventory_create'),
path('inventory/<int:pk>/update/', inventoryView.as_view(), name='inventory_update'),
path('inventory/<int:pk>/delete/', inventoryDeleteView.as_view(), name='inventory_delete'),
]