from django import forms
from core.base_forms import MasterDetailForm
from .models import *

class orderDetailsForm(MasterDetailForm):
    class Meta(MasterDetailForm.Meta):
        model = orderDetails
        fields = '__all__'


class orderHeadersForm(MasterDetailForm):
    class Meta(MasterDetailForm.Meta):
        model = orderHeaders
        fields = '__all__'


