
from rest_framework import viewsets
from customers.models import customer
from customers.serializers.customer_serializer import customerSerializer

class customerViewSet(viewsets.ModelViewSet):
    queryset = customer.objects.all()
    serializer_class = customerSerializer
