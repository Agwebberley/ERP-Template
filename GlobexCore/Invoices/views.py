from django.views.generic import View
from django.shortcuts import render, redirect
from .forms import *


class invoiceDetailsView(View):
    template_name = 'form.html'
    form_class = invoiceDetailsForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        inline_formsets = form.get_inline_formsets()
        return render(request, self.template_name, {'form': form, 'inline_formsets': inline_formsets})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            main_instance = form.save()
            inline_formsets = form.get_inline_formsets(instance=main_instance, data=request.POST, files=request.FILES)
            if all(formset.is_valid() for formset in inline_formsets):
                for formset in inline_formsets:
                    formset.save()
                return redirect(self.success_url)
        inline_formsets = form.get_inline_formsets(data=request.POST, files=request.FILES)
        return render(request, self.template_name, {'form': form, 'inline_formsets': inline_formsets})

class invoiceHeadersView(View):
    template_name = 'form.html'
    form_class = invoiceHeadersForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        inline_formsets = form.get_inline_formsets()
        return render(request, self.template_name, {'form': form, 'inline_formsets': inline_formsets})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            main_instance = form.save()
            inline_formsets = form.get_inline_formsets(instance=main_instance, data=request.POST, files=request.FILES)
            if all(formset.is_valid() for formset in inline_formsets):
                for formset in inline_formsets:
                    formset.save()
                return redirect(self.success_url)
        inline_formsets = form.get_inline_formsets(data=request.POST, files=request.FILES)
        return render(request, self.template_name, {'form': form, 'inline_formsets': inline_formsets})
