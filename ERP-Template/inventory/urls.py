from django.urls import path
from .views import PartListView, PartCreateView, PartUpdateView, PartDetailView, PartDeleteView

urlpatterns = [
    path('part/', PartListView.as_view(), name='part-list'),
    path('part/create/', PartCreateView.as_view(), name='part-create'),
    path('part/<int:pk>/', PartDetailView.as_view(), name='part-detail'),
    path('part/<int:pk>/update/', PartUpdateView.as_view(), name='part-update'),
    path('part/<int:pk>/delete/', PartDeleteView.as_view(), name='part-delete'),
]