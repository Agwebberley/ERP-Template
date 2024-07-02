from django.db import models
from customers.models import Customer
from inventory.models import Part
# Create your models here.

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.part} - {self.quantity}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.order_date}"
