
from rest_framework import viewsets
from core.models import ModelPermissions
from core.serializers.modelpermissions_serializer import ModelPermissionsSerializer

class ModelPermissionsViewSet(viewsets.ModelViewSet):
    queryset = ModelPermissions.objects.all()
    serializer_class = ModelPermissionsSerializer
