
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from customers.models import customer
from customers.serializers.customer_serializer import customerSerializer

class customerViewSet(viewsets.ModelViewSet):
    queryset = customer.objects.all()
    serializer_class = customerSerializer
    permission_classes = [IsAuthenticated]

