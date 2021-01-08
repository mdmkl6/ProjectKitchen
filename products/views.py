from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
# Create your views here.

def products_view(request):
  all_products = Product.objects.all()
  return render(request, 'products.html', {"all_items": all_products})

