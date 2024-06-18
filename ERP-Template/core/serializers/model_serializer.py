
from rest_framework import serializers
from core.models import Model

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'
