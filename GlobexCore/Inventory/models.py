from django.db import models
from Parts.models import parts


class inventory(models.Model):
    LocationID = models.IntegerField()
    QuantityOnHand = models.IntegerField()
    AverageCost = models.IntegerField()
    LastReceivedDate = models.DateTimeField()
    Status = models.CharField(max_length=255)
    PartID = models.ForeignKey(parts, on_delete=models.CASCADE)
