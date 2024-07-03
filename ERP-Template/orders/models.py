from django.db import models
from customers.models import Customer
from inventory.models import Part
# Create your models here.

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.part} - {self.quantity}"
    
    @property
    def total(self):
        return self.part.price * self.quantity

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.order_date}"

    @property
    def total(self):
        order_items = OrderItem.objects.filter(order=self)
        total = sum([item.total for item in order_items])
        return total