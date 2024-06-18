
from rest_framework import serializers
from orders.models import order


from orders.models import order_item


class order_itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_item
        fields = '__all__'


class orderSerializer(serializers.ModelSerializer):
    order_item = order_itemSerializer(many=True)

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
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Handle order items
        for item_data in order_items_data:
            order_item_id = item_data.get('id')
            if order_item_id:
                order_item = order_item.objects.get(id=order_item_id, order=instance)
                order_item.part_id = item_data.get('part_id', order_item.part_id)
                order_item.quantity = item_data.get('quantity', order_item.quantity)
                order_item.unit_price = item_data.get('unit_price', order_item.unit_price)
                order_item.save()
            else:
                order_item.objects.create(order_id=instance, **item_data)
        
        return instance