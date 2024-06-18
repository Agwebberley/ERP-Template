
from rest_framework import serializers
from orders.models import order


from orders.models import order_item


class order_itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_item
        fields = '__all__'


class orderSerializer(serializers.ModelSerializer):
    order_item = order_itemSerializer(many=True, read_only=True)

    class Meta:
        model = order
        fields = '__all__'
