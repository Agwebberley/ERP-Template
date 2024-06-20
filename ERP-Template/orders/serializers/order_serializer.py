
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
        existing_order_items = list(instance.order_item.all())
        updated_order_items = []

        for item_data in order_items_data:
            order_item_id = item_data.get('id')
            if order_item_id:
                order_item_obj = order_item.objects.get(id=order_item_id, order=instance)
                order_item_obj.part_id = item_data.get('part_id', order_item_obj.part_id)
                order_item_obj.quantity = item_data.get('quantity', order_item_obj.quantity)
                order_item_obj.save()
                updated_order_items.append(order_item_obj)
            else:
                item_data.pop('order_id', None)
                new_order_item = order_item.objects.create(**item_data, order_id=instance)
                updated_order_items.append(new_order_item)

        # Remove any order items that were not included in the updated order_items_data
        for existing_item in existing_order_items:
            if existing_item not in updated_order_items:
                existing_item.delete()
        
        return instance

