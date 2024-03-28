from django.db import models
from Parts.models import parts


class invoiceDetails(models.Model):
    InvoiceDetailID = models.IntegerField(primary_key=True)
    InvoiceID = models.IntegerField()
    Description = models.TextField()
    Quantity = models.IntegerField()
    UnitPrice = models.FloatField()
    LineTotal = models.FloatField()
    Discount = models.FloatField()
    TaxRate = models.FloatField()
    TaxAmount = models.FloatField()
    PartID = models.ForeignKey(parts, on_delete=models.CASCADE)


class invoiceHeaders(models.Model):
    InvoiceID = models.IntegerField(primary_key=True)
    OrderID = models.IntegerField()
    CustomerID = models.IntegerField()
    InvoiceDate = models.DateTimeField()
    DueDate = models.DateTimeField()
    TotalAmount = models.FloatField()
    Status = models.CharField(max_length=255)
    TaxAmount = models.FloatField()
    DiscountAmount = models.FloatField()
    ShippingAmount = models.IntegerField()
    PaymentTerms = models.TextField()
    Notes = models.TextField()
