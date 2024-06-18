
from rest_framework import serializers
from orders.models import order_item

class order_itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_item
        fields = '__all__'
