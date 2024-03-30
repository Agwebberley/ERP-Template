from django.db import models

# Create your models here.
class ModelPermissions(models.Model):
    model_name = models.CharField(max_length=255, unique=True)
    can_create = models.BooleanField(default=True)
    can_read = models.BooleanField(default=True)
    can_update = models.BooleanField(default=True)
    can_delete = models.BooleanField(default=True)

    def __str__(self):
        return self.model_name