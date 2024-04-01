from django import forms
from core.base_forms import MasterDetailForm
from core.models import ModelMeta, FieldMeta
from .models import *


class inventoryForm(MasterDetailForm):
    class Meta:
        model = inventory
        try:
            fields = [field.field_name for field in FieldMeta.objects.filter(model=ModelMeta.objects.get(model_name=model._meta.app_label + "." + model.__name__)) if not field.form_hidden]
        except:
            fields = '__all__'
            print("WARNING: Could not retrieve fields for inventory. Using '__all__' instead.")


