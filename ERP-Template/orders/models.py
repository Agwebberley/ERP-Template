from django.db import models
from inventory.models import part


class order(models.Model):
    customer_id = models.IntegerField()
    order_date = models.DateTimeField()
    total_amount = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class order_item(models.Model):
    quantity = models.IntegerField()
    unit_price = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_id = models.ForeignKey('order', on_delete=models.CASCADE)
    part_id = models.ForeignKey(part, on_delete=models.CASCADE)
