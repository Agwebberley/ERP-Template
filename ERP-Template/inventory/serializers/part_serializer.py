
from rest_framework import serializers
from inventory.models import part



class partSerializer(serializers.ModelSerializer):

    class Meta:
        model = part
        fields = '__all__'
