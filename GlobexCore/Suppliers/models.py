from django.db import models


class supplier(models.Model):
    CompanyName = models.CharField(max_length=255)
    ContactTitle = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    IsActive = models.BooleanField()
    Notes = models.TextField()
