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

class ModelMeta(models.Model):
    model_name = models.CharField(max_length=255, unique=True)
    model_verbose_name = models.CharField(max_length=255)
    model_verbose_name_plural = models.CharField(max_length=255)
    model_icon = models.CharField(max_length=255)

    def __str__(self):
        return self.model_name
    
    def get_fields(self):
        return FieldMeta.objects.filter(model=self)

class FieldMeta(models.Model):
    field_name = models.CharField(max_length=255)
    field_verbose_name = models.CharField(max_length=255)
    form_hidden = models.BooleanField(default=False)
    list_hidden = models.BooleanField(default=False)
    field_type = models.CharField(max_length=255)
    field_default = models.CharField(max_length=255)
    model = models.ForeignKey(ModelMeta, on_delete=models.CASCADE)

    # make sure the field name is unique for each model
    class Meta:
        unique_together = ('field_name', 'model')

    def __str__(self):
        return self.model.model_name + "." + self.field_name