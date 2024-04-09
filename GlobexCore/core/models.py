from django.db import models

# Create your models here.

class App(models.Model):
    app_name = models.CharField(max_length=255, unique=True)
    app_verbose_name = models.CharField(max_length=255)
    app_icon = models.CharField(max_length=255)

    def __str__(self):
        return self.app_name


class Model(models.Model):
    model_name = models.CharField(max_length=255)
    model_verbose_name = models.CharField(max_length=255)
    model_icon = models.CharField(max_length=255)
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    # make sure the field name is unique for each model
    class Meta:
        unique_together = ('app', 'model_name')

    def __str__(self):
        return self.app.app_name + "." + self.model_name
    
    def get_fields(self):
        return Field.objects.filter(model=self)


class Field(models.Model):
    field_name = models.CharField(max_length=255)
    field_verbose_name = models.CharField(max_length=255)
    form_hidden = models.BooleanField(default=False)
    list_hidden = models.BooleanField(default=False)
    field_type = models.CharField(max_length=255)
    field_default = models.CharField(max_length=255)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)

    # make sure the field name is unique for each model
    class Meta:
        unique_together = ('field_name', 'model')

    def __str__(self):
        return self.model.model_name + "." + self.field_name

class ModelPermissions(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    can_read = models.BooleanField(default=True)
    can_create = models.BooleanField(default=True)
    can_update = models.BooleanField(default=True)
    can_delete = models.BooleanField(default=True)

    def __str__(self):
        return self.model.model_name + " Permissions"
