from .views import orderDetailsListView, orderDetailsView, orderDetailsDeleteView
from .views import orderHeadersListView, orderHeadersView, orderHeadersDeleteView
from django.urls import path
app_name = 'Orders'
patterns = [

path('orderdetailss/', OrderdetailsListView.as_view(), name='orderdetails_list'),
path('orderdetails/create/', OrderdetailsView.as_view(), name='orderdetails_create'),
path('orderdetails/<int:pk>/update/', OrderdetailsView.as_view(), name='orderdetails_update'),
path('orderdetails/<int:pk>/delete/', OrderdetailsDeleteView.as_view(), name='orderdetails_delete'),

path('orderheaderss/', OrderheadersListView.as_view(), name='orderheaders_list'),
path('orderheaders/create/', OrderheadersView.as_view(), name='orderheaders_create'),
path('orderheaders/<int:pk>/update/', OrderheadersView.as_view(), name='orderheaders_update'),
path('orderheaders/<int:pk>/delete/', OrderheadersDeleteView.as_view(), name='orderheaders_delete'),
]