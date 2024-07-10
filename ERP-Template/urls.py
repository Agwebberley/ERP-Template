"""
URL configuration for ERP-Template project.

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
from inventory.urls import urlpatterns as inventory_urls
from customers.urls import urlpatterns as customers_urls
from orders.urls import urlpatterns as orders_urls
from core.urls import urlpatterns as core_urls
from finance.urls import urlpatterns as finance_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(core_urls)),
    path('inventory/', include(inventory_urls)),
    path('customers/', include(customers_urls)),
    path('orders/', include(orders_urls)),
    path('finance/', include(finance_urls)),
    path('django-rq/', include('django_rq.urls')),
]
