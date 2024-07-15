from django.urls import reverse_lazy
from core.base_views import (
    BaseListView,
    BaseCreateView,
    BaseUpdateView,
    BaseDetailView,
    BaseDeleteView,
)
from .models import Part


# Create your views here.
class PartListView(BaseListView):
    model = Part


class PartCreateView(BaseCreateView):
    model = Part
    success_url = reverse_lazy("part-list")


class PartUpdateView(BaseUpdateView):
    model = Part
    success_url = reverse_lazy("part-list")


class PartDetailView(BaseDetailView):
    model = Part


class PartDeleteView(BaseDeleteView):
    model = Part
    success_url = reverse_lazy("part-list")
