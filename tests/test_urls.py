from django.test import SimpleTestCase
from django.urls import reverse, resolve
from mysite.views import signup
from products.views import products_view
from recipes.views import recipes_view

class TestUrls(SimpleTestCase):

  def test_sing_up_url(self):
    url = reverse('signup')
    self.assertEquals(resolve(url).func,signup)

  def test_recipes(self):
    url = reverse('recipes')
    self.assertEquals(resolve(url).func,recipes_view)

  def test_products(self):
    url = reverse('products')
    self.assertEquals(resolve(url).func,products_view)

#porblem z home view 