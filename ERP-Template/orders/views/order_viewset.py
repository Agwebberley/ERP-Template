
from rest_framework import viewsets
from orders.models import order
from orders.serializers.order_serializer import orderSerializer

class orderViewSet(viewsets.ModelViewSet):
    queryset = order.objects.all()
    serializer_class = orderSerializer
