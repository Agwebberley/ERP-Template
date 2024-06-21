from django.db import models

class Order(models.Model):
    order_date = models.DateTimeField()
    total_amount = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE)


class Order_item(models.Model):
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    part_id = models.ForeignKey('Part', on_delete=models.CASCADE)


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Part(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.CharField(max_length=255)
    stock_quantity = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
