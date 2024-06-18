
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from orders.models import order
from orders.serializers.order_serializer import orderSerializer

class orderViewSet(viewsets.ModelViewSet):
    queryset = order.objects.all()
    serializer_class = orderSerializer
    permission_classes = [IsAuthenticated]

