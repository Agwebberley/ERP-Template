
from rest_framework import viewsets
from core.models import App
from core.serializers.app_serializer import AppSerializer

class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
