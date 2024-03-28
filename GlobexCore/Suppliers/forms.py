from django import forms
from core.base_forms import MasterDetailForm
from .models import *

class supplierForm(MasterDetailForm):
	class Meta:
		model = supplier
		fields = "__all__"

parts = forms.inlineformset_factory(supplier, parts, form=supplierPartsFormSet, extra=1)
class supplierPartsFormSet(forms.BaseInlineFormSet):
	model = parts
	fields = "__all__"
	extra = 1

