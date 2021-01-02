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
def addProducts(request):
    form = ProductsForm(request.POST)

    if form.is_valid():
        new_kitchen = Products(text=request.POST['text'], owner=request.user)
        new_kitchen.save()

    return redirect('kitchen')


def finishedProducts(request, kitchen_id):
    user = request.user
    kitchen = Products.objects.filter(owner=user).get(pk=kitchen_id)
    kitchen.finished = True
    kitchen.save()

    return redirect('kitchen')


def deleteFinished(request):
    user = request.user
    Products.objects.filter(finished__exact =True, owner=user).delete()

    return redirect('kitchen')


def deleteAll(request):
    user = request.user
    Products.objects.filter(owner=user).all().delete()

    return redirect('kitchen')


def autocomplete_kitchen(request):
    if 'term' in request.GET:
        query_set = Product.objects.filter(name__istartswith=request.GET.get('term'))
        products_names = list(map(lambda product: product.name, query_set))
        return JsonResponse(products_names, safe=False)
    return render(request, 'kitchen.html')