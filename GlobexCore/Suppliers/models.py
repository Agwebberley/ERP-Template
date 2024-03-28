from django.db import models


class supplier(models.Model):
    SupplierID = models.IntegerField(primary_key=True)
    CompanyName = models.CharField()
    ContactTitle = models.CharField()
    Address = models.CharField()
    IsActive = models.BooleanField()
    Notes = models.TextField(max_length=255)
