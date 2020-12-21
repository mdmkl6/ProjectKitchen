from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import ToBuy
from .forms import ToBuyForm

# Create your views here.
def shopping_view(request):
  shopping_list = ToBuy.objects.order_by('id')

  form = ToBuyForm()

  context = {'shopping_list' : shopping_list, 'form' : form}
  return render(request, 'shopping.html', context)


@require_POST
def addToBuy(request):
    form = ToBuyForm(request.POST)

    if form.is_valid():
        new_shopping = ToBuy(text=request.POST['text'])
        new_shopping.save()

    return redirect('shopping')



def done(request):
    ToBuy.objects.all().delete()

    return redirect('shopping')
