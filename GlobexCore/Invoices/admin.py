from django.contrib import admin
from core.models import App, Model, Field
from .models import *


class invoiceDetailsAdmin(admin.ModelAdmin):
    model = invoiceDetails

    @property
    def list_display(self):
        try:
            app = App.objects.get(app_name=self.model._meta.app_label)
            return [field.field_name for field in Field.objects.filter(model=Model.objects.get(model_name=self.model.__name__, app=app)) if not field.list_hidden]
        except Exception:
            return ['__str__']  # Default to '__str__' if an error occurs

admin.site.register(invoiceDetails, invoiceDetailsAdmin)

class invoiceHeadersAdmin(admin.ModelAdmin):
    model = invoiceHeaders

    @property
    def list_display(self):
        try:
            app = App.objects.get(app_name=self.model._meta.app_label)
            return [field.field_name for field in Field.objects.filter(model=Model.objects.get(model_name=self.model.__name__, app=app)) if not field.list_hidden]
        except Exception:
            return ['__str__']  # Default to '__str__' if an error occurs

admin.site.register(invoiceHeaders, invoiceHeadersAdmin)
