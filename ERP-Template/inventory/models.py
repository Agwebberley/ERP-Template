from django.db import models


class part(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.CharField(max_length=255)
    stock_quantity = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
