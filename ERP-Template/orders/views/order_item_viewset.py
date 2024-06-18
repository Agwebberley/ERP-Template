
from rest_framework import viewsets
from orders.models import order_item
from orders.serializers.order_item_serializer import order_itemSerializer

class order_itemViewSet(viewsets.ModelViewSet):
    queryset = order_item.objects.all()
    serializer_class = order_itemSerializer
