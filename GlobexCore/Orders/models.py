from django.db import models
from Parts.models import parts


class orderDetails(models.Model):
    Quantity = models.IntegerField()
    UnitPrice = models.FloatField()
    LineTotal = models.CharField(max_length=255)
    Status = models.CharField(max_length=255)
    PartID = models.ForeignKey(parts, on_delete=models.CASCADE)
    OrderID = models.ForeignKey('orderHeaders', on_delete=models.CASCADE)


class orderHeaders(models.Model):
    CustomerID = models.IntegerField()
    OrderDate = models.DateTimeField()
    RequiredDate = models.DateTimeField()
    ShipDate = models.DateTimeField()
    Status = models.CharField(max_length=255)
    ShippingMethod = models.CharField(max_length=255)
    FrieghtCharge = models.FloatField()
    TaxAmount = models.FloatField()
    TotalAmount = models.FloatField()
    PaymentReceived = models.BooleanField()
    Notes = models.TextField()
