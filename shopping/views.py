from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import ToBuy
from .forms import ToBuyForm
from products.models import Product
from kitchen.views import add_if_not_present
from django.http import JsonResponse

# Create your views here.
def shopping_view(request):
  user = request.user
  shopping_list = ToBuy.objects.filter(owner=user).order_by('id')
  form = ToBuyForm()
  context = {'shopping_list' : shopping_list, 'form' : form}
  return render(request, 'shopping.html', context)

@require_POST
def add_to_buy(request):
    form = ToBuyForm(request.POST)
    user = request.user
    shopping_list = ToBuy.objects.filter(owner=user).order_by('id')
    if form.is_valid():
        text = request.POST['text']
        in_products = False
        
        for product in shopping_list:
          if(product.product.name == text):
            return redirect('shopping')

        for product in Product.objects.filter(name__in=[text, text+"s", text+"es"]).all():
          new_shopping = ToBuy(product=product, owner=user, quantity=request.POST['amount'])
          if new_shopping.quantity == 0:
            return redirect('shopping')
          new_shopping.save()
          in_products = True
        
        if not in_products:
          product = Product(name=text)
          product.save()
          new_shopping = ToBuy(product=product, owner=user, quantity=request.POST['amount'])
          new_shopping.save()           
    return redirect('shopping')

def done(request):
    user = request.user
    shopping_list = ToBuy.objects.filter(owner=user).all()
    for item in shopping_list:
      add_if_not_present(item.product.name, item.quantity, user)      
    ToBuy.objects.filter(owner=user).all().delete()
    return redirect('shopping')

def autocomplete_shopping_list(request):
    user = request.user
    if 'term' in request.GET:
        all_products_to_buy_names = list(map(lambda product: product, ToBuy.objects.filter(owner=user)))
        found_products = Product.objects.filter(name__istartswith=request.GET.get('term'))
        products_names = []
        found_product_index = 0
        for product in found_products:
            if product.name not in all_products_to_buy_names:
                products_names.insert(found_product_index, product.name)
                found_product_index += 1
            else:
                products_names.append(product.name)
        return JsonResponse(products_names, safe=False)
    return render(request, 'shopping.html')
