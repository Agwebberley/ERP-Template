from django.db import models


class orderDetails(models.Model):
    OrderDetailID = models.IntegerField(primary_key=True)
    PartID = models.IntegerField()
    Quantity = models.IntegerField()
    UnitPrice = models.FloatField()
    LineTotal = models.CharField()
    Status = models.CharField()
    OrderID = models.ForeignKey('orderHeaders', on_delete=models.CASCADE)


class orderHeaders(models.Model):
    OrderID = models.IntegerField(primary_key=True)
    CustomerID = models.IntegerField()
    OrderDate = models.DateTimeField()
    RequiredDate = models.DateTimeField()
    ShipDate = models.DateTimeField()
    Status = models.CharField()
    ShippingMethod = models.CharField()
    FrieghtCharge = models.FloatField()
    TaxAmount = models.FloatField()
    TotalAmount = models.FloatField()
    PaymentReceived = models.BooleanField()
    Notes = models.TextField(max_length=255)
