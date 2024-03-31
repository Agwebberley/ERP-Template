from django.db import models


class Customer(models.Model):
    CompanyName = models.CharField(max_length=255)
    ContactName = models.CharField(max_length=255)
    ContactTitle = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    State = models.CharField(max_length=255)
    PostalCode = models.IntegerField()
    Phone = models.IntegerField()
    Email = models.CharField(max_length=255)
    IsActive = models.BooleanField()
    Notes = models.TextField()
