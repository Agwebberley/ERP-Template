from .views import orderDetailsListView, orderDetailsView, orderDetailsDeleteView
from .views import orderHeadersListView, orderHeadersView, orderHeadersDeleteView
from django.urls import path
app_name = 'Orders'
patterns = [

path('orderdetailss/', orderDetailsListView.as_view(), name='orderdetails_list'),
path('orderdetails/create/', orderDetailsView.as_view(), name='orderdetails_create'),
path('orderdetails/<int:pk>/update/', orderDetailsView.as_view(), name='orderdetails_update'),
path('orderdetails/<int:pk>/delete/', orderDetailsDeleteView.as_view(), name='orderdetails_delete'),

path('orderheaderss/', orderHeadersListView.as_view(), name='orderheaders_list'),
path('orderheaders/create/', orderHeadersView.as_view(), name='orderheaders_create'),
path('orderheaders/<int:pk>/update/', orderHeadersView.as_view(), name='orderheaders_update'),
path('orderheaders/<int:pk>/delete/', orderHeadersDeleteView.as_view(), name='orderheaders_delete'),
]