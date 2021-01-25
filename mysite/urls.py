"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from mysite import views
from django.views.generic.base import TemplateView
from products.views import products_view



urlpatterns = [
    path('admin/', admin.site.urls), 
    url('signup/', views.signup, name='signup'),  
    path('', include('django.contrib.auth.urls')),
    path('',views.home, name='home'),
    path('products/', products_view, name='products'),
    path('recipes/', include('recipes.urls')),
    path('', include('kitchen.urls')),
    path('', include('shopping.urls'))  
  ]
