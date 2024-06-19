
from rest_framework import serializers
from orders.models import order


from orders.serializers.order_item_serializer import order_itemSerializer
from orders.models import order_item

class orderSerializer(serializers.ModelSerializer):
    order_item = order_itemSerializer(many=True)
    total = serializers.DecimalField(source="get_total_price", max_digits=10, decimal_places=2, read_only=True)


    class Meta:
        model = order
        fields = '__all__'

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_item')
        Order = order.objects.create(**validated_data)
        for item_data in order_items_data:
            order_item.objects.create(order_id=Order, **item_data)
        return Order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_item')
        instance.customer_id = validated_data.get('customer_id', instance.customer_id)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Handle order items
        for item_data in order_items_data:
            order_item_id = item_data.get('id')
            if order_item_id:
                order_item = order_item.objects.get(id=order_item_id, order=instance)
                order_item.part_id = item_data.get('part_id', order_item.part_id)
                order_item.quantity = item_data.get('quantity', order_item.quantity)
                order_item.save()
            else:
                order_item.objects.create(order_id=instance, **item_data)
        
        return instance

