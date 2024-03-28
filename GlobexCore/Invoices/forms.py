from django import forms
from core.base_forms import MasterDetailForm
from .models import *

class invoiceDetailsForm(MasterDetailForm):
    class Meta(MasterDetailForm.Meta):
        model = invoiceDetails
        fields = '__all__'


class invoiceHeadersForm(MasterDetailForm):
    class Meta(MasterDetailForm.Meta):
        model = invoiceHeaders
        fields = '__all__'


