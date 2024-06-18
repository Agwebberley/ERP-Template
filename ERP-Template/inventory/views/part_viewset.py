
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from inventory.models import part
from inventory.serializers.part_serializer import partSerializer

class partViewSet(viewsets.ModelViewSet):
    queryset = part.objects.all()
    serializer_class = partSerializer
    permission_classes = [IsAuthenticated]

