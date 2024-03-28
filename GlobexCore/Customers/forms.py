from django import forms
from core.base_forms import MasterDetailForm
from .models import *

class CustomerForm(MasterDetailForm):
	class Meta:
		model = Customer
		fields = "__all__"

