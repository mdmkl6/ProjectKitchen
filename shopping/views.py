from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import ToBuy
from .forms import ToBuyForm

from products.models import Product
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
        new_shopping = ToBuy(text=request.POST['text'], owner=request.user, amount=request.POST['amount'])
        for product in shopping_list:
          if product.text == new_shopping.text:
            return redirect('shopping')
        new_shopping.save()

    return redirect('shopping')



def done(request):
    user = request.user
    ToBuy.objects.filter(owner=user).all().delete()

    return redirect('shopping')

    
def autocomplete_shopping_list(request):
    user = request.user
    if 'term' in request.GET:
        all_products_to_buy_names = list(map(lambda product: product.text, 
                                             ToBuy.objects.filter(owner=user)))

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
