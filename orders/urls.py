from django.urls import path
from orders.views import (
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
)

urlpatterns = [
    path("list/", OrderListView.as_view(), name="order-list"),
    path(
        "create/",
        OrderCreateView.as_view(),
        {"app_label": "orders", "model_name": "Order"},
        name="order-create",
    ),
    path(
        "update/<int:pk>/",
        OrderUpdateView.as_view(),
        {"app_label": "orders", "model_name": "Order"},
        name="order-update",
    ),
    path("delete/<int:pk>/", OrderDeleteView.as_view(), name="order-delete"),
    path("detail/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]
