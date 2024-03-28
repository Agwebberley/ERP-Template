from django import forms
from core.base_forms import MasterDetailForm
from .models import *

class orderDetailsForm(MasterDetailForm):
	class Meta:
		model = orderDetails
		fields = "__all__"

class orderHeadersForm(MasterDetailForm):
	class Meta:
		model = orderHeaders
		fields = "__all__"

orderDetails = forms.inlineformset_factory(orderHeaders, orderDetails, form=orderHeadersOrderdetailsFormSet, extra=1)
class orderHeadersOrderdetailsFormSet(forms.BaseInlineFormSet):
	model = orderDetails
	fields = "__all__"
	extra = 1

