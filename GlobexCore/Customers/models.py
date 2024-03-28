from django.db import models


class Customer(models.Model):
    CustomerID = models.IntegerField(primary_key=True)
    CompanyName = models.CharField()
    ContactName = models.CharField()
    ContactTitle = models.CharField()
    Address = models.CharField()
    City = models.CharField()
    State = models.CharField()
    PostalCode = models.IntegerField()
    Phone = models.IntegerField()
    Email = models.CharField()
    IsActive = models.BooleanField()
    Notes = models.TextField(max_length=255)
