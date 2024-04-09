from django.contrib import admin
from core.models import App, Model, Field
from .models import *


class AppAdmin(admin.ModelAdmin):
    model = App

    @property
    def list_display(self):
        try:
            app = App.objects.get(app_name=self.model._meta.app_label)
            return [field.field_name for field in Field.objects.filter(model=Model.objects.get(model_name=self.model.__name__, app=app)) if not field.list_hidden]
        except Exception:
            return ['__str__']  # Default to '__str__' if an error occurs

admin.site.register(App, AppAdmin)

class ModelAdmin(admin.ModelAdmin):
    model = Model

    @property
    def list_display(self):
        try:
            app = App.objects.get(app_name=self.model._meta.app_label)
            return [field.field_name for field in Field.objects.filter(model=Model.objects.get(model_name=self.model.__name__, app=app)) if not field.list_hidden]
        except Exception:
            return ['__str__']  # Default to '__str__' if an error occurs

admin.site.register(Model, ModelAdmin)

class FieldAdmin(admin.ModelAdmin):
    model = Field

    @property
    def list_display(self):
        try:
            app = App.objects.get(app_name=self.model._meta.app_label)
            return [field.field_name for field in Field.objects.filter(model=Model.objects.get(model_name=self.model.__name__, app=app)) if not field.list_hidden]
        except Exception:
            return ['__str__']  # Default to '__str__' if an error occurs

admin.site.register(Field, FieldAdmin)

class ModelPermissionsAdmin(admin.ModelAdmin):
    model = ModelPermissions

    @property
    def list_display(self):
        try:
            app = App.objects.get(app_name=self.model._meta.app_label)
            return [field.field_name for field in Field.objects.filter(model=Model.objects.get(model_name=self.model.__name__, app=app)) if not field.list_hidden]
        except Exception:
            return ['__str__']  # Default to '__str__' if an error occurs

admin.site.register(ModelPermissions, ModelPermissionsAdmin)
