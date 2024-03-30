from django import forms
from core.base_forms import MasterDetailForm
from .models import *

class supplierForm(MasterDetailForm):
	class Meta:
		model = supplier
		fields = "__all__"

