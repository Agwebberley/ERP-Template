
from rest_framework import viewsets
from core.models import Field
from core.serializers.field_serializer import FieldSerializer

class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
