
from rest_framework import viewsets
from inventory.models import part
from inventory.serializers.part_serializer import partSerializer

class partViewSet(viewsets.ModelViewSet):
    queryset = part.objects.all()
    serializer_class = partSerializer
