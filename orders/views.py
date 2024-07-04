from django.shortcuts import render
from django.urls import reverse_lazy
from core.base_views import BaseListView, BaseDeleteView, BaseMasterDetailView, MasterDetailUpdateView, MasterDetailCreateView
from .models import Order, OrderItem
# Create your views here.

class OrderListView(BaseListView):
    model = Order

class OrderCreateView(MasterDetailCreateView):
    model = Order
    success_url = reverse_lazy('order-list')

class OrderUpdateView(MasterDetailUpdateView):
    model = Order
    success_url = reverse_lazy('order-list')

class OrderDeleteView(BaseDeleteView):
    model = Order
    success_url = reverse_lazy('order-list')

class OrderDetailView(BaseMasterDetailView):
    model = Order