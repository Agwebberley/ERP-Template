from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect

class BaseFormWithInlineFormsetView(CreateView, UpdateView):
    model = None  # This should be overridden in the subclass
    form_class = None  # This should be overridden in the subclass
    inline_formset_classes = []  # List of inline formset classes
    template_name = 'form.html'
    success_url = reverse_lazy('/')  # Override this in subclasses

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            # If a primary key (pk) is provided in the URL, treat this as a detail or update view
            instance = self.model.objects.get(pk=kwargs['pk'])
            form = self.form_class(instance=instance)
            inline_formsets = form.get_inline_formsets(instance=instance)
            return render(request, 'detail_or_update_template.html', {'form': form, 'inline_formsets': inline_formsets})
        else:
            # If no pk is provided, treat this as a create view
            form = self.form_class()
            inline_formsets = form.get_inline_formsets()
            return render(request, self.template_name, {'form': form, 'inline_formsets': inline_formsets})

    def post(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            instance = self.model.objects.get(pk=kwargs['pk'])
            form = self.form_class(data=request.POST, files=request.FILES, instance=instance)
        else:
            form = self.form_class(data=request.POST, files=request.FILES)

        if form.is_valid():
            main_instance = form.save()
            inline_formsets = form.get_inline_formsets(instance=main_instance, data=request.POST, files=request.FILES)
            if all(formset.is_valid() for formset in inline_formsets):
                for formset in inline_formsets:
                    formset.save()
                return redirect(self.success_url)

        inline_formsets = form.get_inline_formsets(data=request.POST, files=request.FILES, instance=instance if 'pk' in kwargs else None)
        return render(request, self.template_name if 'pk' not in kwargs else 'detail_or_update_template.html', {'form': form, 'inline_formsets': inline_formsets})

