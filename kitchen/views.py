from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Products
from .forms import ProductsForm
from products.models import Product
from django.http import JsonResponse

# Create your views here.
def kitchen_view(request):
  user = request.user
  kitchen_list = Products.objects.filter(owner=user).order_by('id')
  form = ProductsForm()
  context = {'kitchen_list' : kitchen_list, 'form' : form}
  
  return render(request, 'kitchen.html', context)

@require_POST
def add_products(request):
    form = ProductsForm(request.POST)
    user = request.user
    kitchen_list = Products.objects.filter(owner=user).order_by('id')
    if form.is_valid():
        text = request.POST['text']
        in_products = False
        
        for product in kitchen_list:
          if(product.product.name == text):
            return redirect('kitchen')

        for product in Product.objects.filter(name__in=[text, text+"s", text+"es"]).all():
          new_kitchen = Products(product=product, owner=user, quantity=request.POST['amount'])
          if new_kitchen.quantity == 0:
            new_kitchen.finished = True
          new_kitchen.save()
          in_products = True
        if not in_products:
          product = Product(name=text)
          product.save()
          new_kitchen = Products(product=product, owner=user, quantity=request.POST['amount'])
          new_kitchen.save()          
    
    return redirect('kitchen')

def finished_products(request, kitchen_id):
    user = request.user
    kitchen = Products.objects.filter(owner=user).get(pk=kitchen_id)
    kitchen.quantity = 0
    kitchen.finished = True
    kitchen.save()
    
    return redirect('kitchen')

def change_amount(request, product_id):
    user = request.user
    product = Products.objects.filter(owner=user).get(pk=product_id)
    product.quantity = request.POST['amount']
    if product.quantity == 0:
      product.finished = True
    product.save()    
    
    return redirect('kitchen')

def delete_finished(request):
    user = request.user
    Products.objects.filter(finished__exact=True, owner=user).delete()
    
    return redirect('kitchen')

def delete_all(request):
    user = request.user
    Products.objects.filter(owner=user).all().delete()
    
    return redirect('kitchen')

def autocomplete_kitchen(request):
    if 'term' in request.GET:
        found_products = Product.objects.filter(name__istartswith=request.GET.get('term'))
        products_names = list(map(lambda product: product.name, found_products))
        return JsonResponse(products_names, safe=False)
    return render(request, 'kitchen.html')
    