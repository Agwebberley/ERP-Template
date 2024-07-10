from django.urls import path
from core.base_views import HomeView, LoginView, LogoutView, LogMessageView, LogMessageDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('log/', LogMessageView.as_view(), name='logmessage-list'),
    path('log/<int:pk>/', LogMessageDetailView.as_view(), name='logmessage-detail'),
]