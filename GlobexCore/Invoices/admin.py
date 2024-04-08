from django.contrib import admin
from core.models import ModelMeta, FieldMeta
from .models import *


class invoiceDetailsAdmin(admin.ModelAdmin):
    model = invoiceDetails

    @property
    def list_display(self):
        try:
            return [field.field_name for field in FieldMeta.objects.filter(model=ModelMeta.objects.get(model_name=self.model._meta.app_label + "." + self.model.__name__)) if not field.list_hidden]
        except Exception:
            return ['__str__']  # Default to '__str__' if an error occurs

admin.site.register(invoiceDetails, invoiceDetailsAdmin)

class invoiceHeadersAdmin(admin.ModelAdmin):
    model = invoiceHeaders

    @property
    def list_display(self):
        try:
            return [field.field_name for field in FieldMeta.objects.filter(model=ModelMeta.objects.get(model_name=self.model._meta.app_label + "." + self.model.__name__)) if not field.list_hidden]
        except Exception:
            return ['__str__']  # Default to '__str__' if an error occurs

admin.site.register(invoiceHeaders, invoiceHeadersAdmin)
