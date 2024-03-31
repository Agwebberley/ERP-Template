from .views import inventoryListView, inventoryCreateView, inventoryUpdateView, inventoryDeleteView
from django.urls import path
app_name = 'Inventory'
urlpatterns = [

path('inventorys/', inventoryListView.as_view(), name='inventory_list'),
path('inventory/create/', inventoryCreateView.as_view(), name='inventory_create'),
path('inventory/<int:pk>/update/', inventoryUpdateView.as_view(), name='inventory_update'),
path('inventory/<int:pk>/delete/', inventoryDeleteView.as_view(), name='inventory_delete'),
]