from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import ToBuy
from .forms import ToBuyForm

# Create your views here.
def shopping_view(request):
  user = request.user
  shopping_list = ToBuy.objects.filter(owner=user).order_by('id')

  form = ToBuyForm()

  context = {'shopping_list' : shopping_list, 'form' : form}
  return render(request, 'shopping.html', context)


@require_POST
def addToBuy(request):
    form = ToBuyForm(request.POST)

    if form.is_valid():
        new_shopping = ToBuy(text=request.POST['text'], owner=request.user)
        new_shopping.save()

    return redirect('shopping')



def done(request):
    user = request.user
    ToBuy.objects.filter(owner=user).all().delete()

    return redirect('shopping')