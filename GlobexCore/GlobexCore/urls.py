"""
URL configuration for GlobexCore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("authentication.urls")), # Auth routes - login / register
]
urlpatterns.append(path('Customers/', include('Customers.urls')))
urlpatterns.append(path('', include('core.urls')))
urlpatterns.append(path('Inventory/', include('Inventory.urls')))
urlpatterns.append(path('Orders/', include('Orders.urls')))
urlpatterns.append(path('Invoices/', include('Invoices.urls')))
urlpatterns.append(path('Parts/', include('Parts.urls')))
urlpatterns.append(path('Suppliers/', include('Suppliers.urls')))