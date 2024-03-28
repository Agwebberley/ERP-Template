from django.db import models
from Parts import parts


class inventory(models.Model):
    InventoryID = models.IntegerField(primary_key=True)
    LocationID = models.IntegerField()
    QuantityOnHand = models.IntegerField()
    AverageCost = models.IntegerField()
    LastReceivedDate = models.DateTimeField()
    Status = models.CharField()
    PartID = models.ForeignKey(parts, on_delete=models.CASCADE)
