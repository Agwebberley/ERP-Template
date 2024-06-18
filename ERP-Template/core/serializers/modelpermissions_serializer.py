
from rest_framework import serializers
from core.models import ModelPermissions

class ModelPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelPermissions
        fields = '__all__'
