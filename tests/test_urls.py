from django.test import SimpleTestCase
from django.urls import reverse, resolve
from mysite.views import signup,home
from products.views import products_view
from recipes.views import recipes_view
from kitchen.views import kitchen_view, add_products, finished_products,change_amount, delete_finished, delete_all,autocomplete_kitchen
from shopping.views import shopping_view, add_to_buy, done, autocomplete_shopping_list



class TestUrls(SimpleTestCase):

  def test_sing_up_url(self):
    url = reverse('signup')
    self.assertEquals(resolve(url).func,signup)

  def test_home_url(self):
    url = reverse('home')
    self.assertEquals(resolve(url).func,home)

  #def test_login_url(self):
    #url=reverse('login')
    #self.assertEquals(resolve(url).func,django.contrib.auth.views)

################################################################3

  def test_recipes_url(self):
    url = reverse('recipes')
    self.assertEquals(resolve(url).func,recipes_view)

  def test_products_url(self):
    url = reverse('products')
    self.assertEquals(resolve(url).func,products_view)

##########################################################

  def test_kitchen_url(self):
    url = reverse('kitchen')
    self.assertEquals(resolve(url).func,kitchen_view)
  
  def test_kitchen_add_url(self):
    url = reverse('add')
    self.assertEquals(resolve(url).func,add_products)

  def test_kitchen_finished_url(self):
    url = reverse('finished',args=['product'])
    self.assertEquals(resolve(url).func,finished_products)

  def test_kitchen_deletefinished_url(self):
    url = reverse('deletefinished')
    self.assertEquals(resolve(url).func,delete_finished)

  def test_kitchen_deleteall_url(self):
    url = reverse('deleteall')
    self.assertEquals(resolve(url).func,delete_all)

#########################################################

  def test_shopping_url(self):
    url = reverse('shopping')
    self.assertEquals(resolve(url).func,shopping_view)

  def test_shopping_add_to_buy_url(self):
    url = reverse('add_to_buy')
    self.assertEquals(resolve(url).func,add_to_buy)

  def test_shopping_done_url(self):
    url = reverse('done')
    self.assertEquals(resolve(url).func,done)
 
  