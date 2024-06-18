
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views.app_viewset import AppViewSet
from core.views.model_viewset import ModelViewSet
from core.views.field_viewset import FieldViewSet
from core.views.modelpermissions_viewset import ModelPermissionsViewSet
from customers.views.customer_viewset import customerViewSet
from inventory.views.part_viewset import partViewSet
from orders.views.order_viewset import orderViewSet
from orders.views.order_item_viewset import order_itemViewSet

router = DefaultRouter()
router.register(r'app', AppViewSet)
router.register(r'model', ModelViewSet)
router.register(r'field', FieldViewSet)
router.register(r'modelpermissions', ModelPermissionsViewSet)
router.register(r'customer', customerViewSet)
router.register(r'part', partViewSet)
router.register(r'order', orderViewSet)
router.register(r'order_item', order_itemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
