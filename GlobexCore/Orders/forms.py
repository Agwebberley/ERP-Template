from django import forms
from core.base_forms import MasterDetailForm
from core.models import ModelMeta, FieldMeta
from .models import *


class orderDetailsForm(MasterDetailForm):
    class Meta:
        model = orderDetails
        try:
            fields = [field.field_name for field in FieldMeta.objects.filter(model=ModelMeta.objects.get(model_name=model._meta.app_label + "." + model.__name__)) if not field.form_hidden]
        except:
            fields = '__all__'
            print("WARNING: Could not retrieve fields for orderDetails. Using '__all__' instead.")


class orderHeadersOrderdetailsFormSet(forms.BaseInlineFormSet):
	model = orderDetails
	fields = "__all__"
	extra = 1


class orderHeadersForm(MasterDetailForm):
    class Meta:
        model = orderHeaders
        try:
            fields = [field.field_name for field in FieldMeta.objects.filter(model=ModelMeta.objects.get(model_name=model._meta.app_label + "." + model.__name__)) if not field.form_hidden]
        except:
            fields = '__all__'
            print("WARNING: Could not retrieve fields for orderHeaders. Using '__all__' instead.")

orderDetails = forms.inlineformset_factory(orderHeaders, orderDetails, form=orderHeadersOrderdetailsFormSet, extra=1, fields='__all__')

