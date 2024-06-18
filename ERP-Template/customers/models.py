from django.db import models


class customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
