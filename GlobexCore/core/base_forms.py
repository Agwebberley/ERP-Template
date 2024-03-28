from django import forms
from django.forms.models import inlineformset_factory

class MasterDetailForm(forms.ModelForm):
    # This base class can be used for all forms, now focusing on inline formset support

    @staticmethod
    def get_inline_formset(related_model, form, fk_name, extra=1, can_delete=True, fields='__all__', **kwargs):
        """
        Creates an inline formset for related models.

        :param related_model: The related model class.
        :param form: The form class for the related model.
        :param fk_name: The name of the ForeignKey field in the related model that points back to the master model.
        :param extra: The number of extra forms in the formset.
        :param can_delete: Whether forms in the formset can be deleted.
        :param fields: The fields of the related model to include in the formset.
        :return: An inline formset class.
        """
        return inlineformset_factory(
            self.Meta.model, related_model,
            form=form,
            fk_name=fk_name,
            fields=fields,
            extra=extra,
            can_delete=can_delete,
            **kwargs
        )
