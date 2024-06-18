
from rest_framework import viewsets
from core.models import Model
from core.serializers.model_serializer import ModelSerializer

class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
