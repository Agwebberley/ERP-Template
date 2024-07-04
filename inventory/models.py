from django.db import models

# Create your models here.
class Part(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    part_number = models.CharField(max_length=255, unique=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name