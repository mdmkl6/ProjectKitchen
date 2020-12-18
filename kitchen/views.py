from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Products
from .forms import ProductsForm

# Create your views here.
def kitchen_view(request):
  kitchen_list = Products.objects.order_by('id')

  form = ProductsForm()

  context = {'kitchen_list' : kitchen_list, 'form' : form}
  return render(request, 'kitchen.html', context)


@require_POST
def addProducts(request):
    form = ProductsForm(request.POST)

    if form.is_valid():
        new_kitchen = Products(text=request.POST['text'])
        new_kitchen.save()

    return redirect('kitchen')

def finishedProducts(request, kitchen_id):
    kitchen = Products.objects.get(pk=kitchen_id)
    kitchen.finished = True
    kitchen.save()

    return redirect('kitchen')

def deleteFinished(request):
    Products.objects.filter(finished__exact =True).delete()

    return redirect('kitchen')

def deleteAll(request):
    Products.objects.all().delete()

    return redirect('kitchen')
