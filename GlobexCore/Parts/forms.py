from django import forms
from core.base_forms import MasterDetailForm
from .models import *

class partsForm(MasterDetailForm):
    class Meta(MasterDetailForm.Meta):
        model = parts
        fields = '__all__'


