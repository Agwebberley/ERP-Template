from django.db import models
from core.models import BaseModel


# Create your models here.
class Customer(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name
