
from rest_framework import serializers
from orders.models import order_item



class order_itemSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(source="get_line_total", max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = order_item
        fields = '__all__'
