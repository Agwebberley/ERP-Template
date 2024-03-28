from django import forms
from core.base_forms import MasterDetailForm
from .models import *

class inventoryForm(MasterDetailForm):
	class Meta:
		model = inventory
		fields = "__all__"

