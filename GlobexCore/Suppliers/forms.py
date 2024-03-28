from django import forms
from core.base_forms import MasterDetailForm
from .models import *

class supplierForm(MasterDetailForm):
    class Meta(MasterDetailForm.Meta):
        model = supplier
        fields = '__all__'


