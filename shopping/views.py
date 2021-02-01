from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import ToBuy
from products.models import Product
from .forms import ToBuyForm
from kitchen.views import add_to_kitchen_or_change_amount


def shopping_view(request):
  user = request.user
  shopping_list = ToBuy.objects.filter(owner=user).order_by('id')
  form = ToBuyForm()
  context = {'shopping_list' : shopping_list, 'form' : form}
  return render(request, 'shopping.html', context)


def ignore_item_if_already_present(text, user):
  shopping_list = ToBuy.objects.filter(owner=user).order_by('id')
  for product in shopping_list:
    if(product.product.name == text):
      return redirect('shopping')


def check_item_and_add_if_exists(text, amount, user):
  name_with_plural_forms = [text, f"{text}s", f"{text}es", f"{text[:-1]}", f"{text[:-2]}", f"{text[:-1]}ies"]
  for product in Product.objects.filter(name__in=name_with_plural_forms).all():
    new_shopping = ToBuy(product=product, owner=user, quantity=amount)
    if new_shopping.quantity != 0:
      new_shopping.save()
    return True
    

def add_non_existing_item(text, amount, user):
  product = Product(name=text)
  product.save()
  new_shopping = ToBuy(product=product, owner=user, quantity=amount)
  new_shopping.save()           


@require_POST
def add_to_buy(request):
  form = ToBuyForm(request.POST)
  user = request.user
  if form.is_valid():
      text = request.POST['text']
      amount = request.POST['amount']
      ignore_item_if_already_present(text, user)        
      item_exists = check_item_and_add_if_exists(text, amount, user)
      if not item_exists:
        add_non_existing_item(text, amount, user)
  return redirect('shopping')


def done(request):
    user = request.user
    shopping_list = ToBuy.objects.filter(owner=user).all()
    for item in shopping_list:
      add_to_kitchen_or_change_amount(item.product.name, item.quantity, user)      
    ToBuy.objects.filter(owner=user).all().delete()
    return redirect('shopping')


def autocomplete_shopping_list(request):
    user = request.user
    if 'term' in request.GET:
        all_products_to_buy_names = ToBuy.objects.filter(owner=user)
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
