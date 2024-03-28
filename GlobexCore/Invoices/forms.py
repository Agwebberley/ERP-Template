from django import forms
from core.base_forms import MasterDetailForm
from .models import *

class invoiceDetailsForm(MasterDetailForm):
	class Meta:
		model = invoiceDetails
		fields = "__all__"

class invoiceHeadersForm(MasterDetailForm):
	class Meta:
		model = invoiceHeaders
		fields = "__all__"

