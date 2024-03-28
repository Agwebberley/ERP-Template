from django.db import models
from Suppliers.models import supplier


class parts(models.Model):
    PartID = models.IntegerField(primary_key=True)
    PartName = models.CharField(max_length=255)
    Description = models.TextField()
    CatagoryID = models.IntegerField()
    Price = models.FloatField()
    Cost = models.FloatField()
    MinimumStockLevel = models.IntegerField()
    ReorderQuantity = models.IntegerField()
    LeadTime = models.IntegerField()
    SupplierID = models.ForeignKey(supplier, on_delete=models.CASCADE)
