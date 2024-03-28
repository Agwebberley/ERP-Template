from django import forms
from core.base_forms import MasterDetailForm
from .models import *

class partsForm(MasterDetailForm):
	class Meta:
		model = parts
		fields = "__all__"

inventory = forms.inlineformset_factory(parts, inventory, form=partsInventoryFormSet, extra=1)
orderDetails = forms.inlineformset_factory(parts, orderDetails, form=partsOrderdetailsFormSet, extra=1)
invoiceDetails = forms.inlineformset_factory(parts, invoiceDetails, form=partsInvoicedetailsFormSet, extra=1)
class partsInventoryFormSet(forms.BaseInlineFormSet):
	model = inventory
	fields = "__all__"
	extra = 1

class partsOrderdetailsFormSet(forms.BaseInlineFormSet):
	model = orderDetails
	fields = "__all__"
	extra = 1

class partsInvoicedetailsFormSet(forms.BaseInlineFormSet):
	model = invoiceDetails
	fields = "__all__"
	extra = 1

