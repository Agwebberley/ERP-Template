from django.db import models
from Parts import parts


class invoiceDetails(models.Model):
    InvoiceDetailID = models.IntegerField(primary_key=True)
    InvoiceID = models.IntegerField()
    Description = models.TextField(max_length=255)
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
    Status = models.CharField()
    TaxAmount = models.FloatField()
    DiscountAmount = models.FloatField()
    ShippingAmount = models.IntegerField()
    PaymentTerms = models.TextField(max_length=255)
    Notes = models.TextField(max_length=255)
