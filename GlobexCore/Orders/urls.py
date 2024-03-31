from .views import orderDetailsListView, orderDetailsCreateView, orderDetailsUpdateView, orderDetailsDeleteView
from .views import orderHeadersListView, orderHeadersCreateView, orderHeadersUpdateView, orderHeadersDeleteView
from django.urls import path
app_name = 'Orders'
urlpatterns = [

path('orderdetailss/', orderDetailsListView.as_view(), name='orderdetails_list'),
path('orderdetails/create/', orderDetailsCreateView.as_view(), name='orderdetails_create'),
path('orderdetails/<int:pk>/update/', orderDetailsUpdateView.as_view(), name='orderdetails_update'),
path('orderdetails/<int:pk>/delete/', orderDetailsDeleteView.as_view(), name='orderdetails_delete'),

path('orderheaderss/', orderHeadersListView.as_view(), name='orderheaders_list'),
path('orderheaders/create/', orderHeadersCreateView.as_view(), name='orderheaders_create'),
path('orderheaders/<int:pk>/update/', orderHeadersUpdateView.as_view(), name='orderheaders_update'),
path('orderheaders/<int:pk>/delete/', orderHeadersDeleteView.as_view(), name='orderheaders_delete'),
]