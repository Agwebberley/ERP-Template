from django.db import models
from django.db.models import Sum, F  # Import Sum and F from django.db.models
from inventory.models import part


class order_item(models.Model):
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_id = models.ForeignKey('order', on_delete=models.CASCADE, related_name='order_item', blank=True, null=True)
    part_id = models.ForeignKey(part, on_delete=models.CASCADE)

    def get_line_total(self):
        return self.quantity * self.part_id.price


class order(models.Model):
    customer_id = models.IntegerField()
    order_date = models.DateTimeField()
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def get_total_price(self):
        total = sum(item.quantity * item.part_id.price for item in self.order_item.all())
        return total
