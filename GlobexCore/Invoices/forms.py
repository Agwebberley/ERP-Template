from django import forms
from core.base_forms import MasterDetailForm
from core.models import ModelMeta, FieldMeta
from .models import *


class invoiceDetailsForm(MasterDetailForm):
    class Meta:
        model = invoiceDetails
        try:
            fields = [field.field_name for field in FieldMeta.objects.filter(model=ModelMeta.objects.get(model_name=model._meta.app_label + "." + model.__name__)) if not field.form_hidden]
        except:
            fields = '__all__'
            print("WARNING: Could not retrieve fields for invoiceDetails. Using '__all__' instead.")



class invoiceHeadersForm(MasterDetailForm):
    class Meta:
        model = invoiceHeaders
        try:
            fields = [field.field_name for field in FieldMeta.objects.filter(model=ModelMeta.objects.get(model_name=model._meta.app_label + "." + model.__name__)) if not field.form_hidden]
        except:
            fields = '__all__'
            print("WARNING: Could not retrieve fields for invoiceHeaders. Using '__all__' instead.")


