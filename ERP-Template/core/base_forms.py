from django import forms
from django.forms.models import inlineformset_factory

class MasterDetailForm(forms.ModelForm):
    # This base class can be used for all forms, now focusing on inline formset support

    @classmethod
    def get_inline_formsets(cls, instance=None, data=None, files=None):
        # This method should return a list of instantiated inline formsets
        formsets = []
        for related_object in cls.Meta.model._meta.related_objects:
            # Assuming a ForeignKey relationship for simplicity; adjust as needed
            if related_object.one_to_many:
                Formset = inlineformset_factory(
                    cls.Meta.model, related_object.related_model,
                    fields='__all__', extra=1, can_delete=True
                )
                formset = Formset(data=data, files=files, instance=instance)
                formsets.append(formset)
        return formsets