from core.base_views import BaseListView, BaseDetailView
from .models import Invoice


class InvoiceListView(BaseListView):
    model = Invoice


class InvoiceDetailView(BaseDetailView):
    model = Invoice
