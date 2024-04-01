from django.contrib import admin

# Register your models here.
from .models import ModelPermissions, ModelMeta, FieldMeta

admin.site.register(ModelPermissions)
admin.site.register(ModelMeta)
admin.site.register(FieldMeta)

