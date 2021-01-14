from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login
from shopping.forms import ToBuyForm


class TestViews(TestCase):

  def setUp(self):
    user = User.objects.create(username='user1')
    user.set_password('haslo1234')
    user.save() 
    self.client=Client()
    self.client.login(username='user1', password='haslo1234')


    self.home_url=reverse('home')
    self.signup_url=reverse('signup')

    self.products_url=reverse('products')
    self.recipes_url=reverse('recipes')

    self.kitchen_url=reverse('kitchen')
    self.kitchen_add_url=reverse('add')
    #self.kitchen_finished_url=reverse('finished')
    self.kitchen_delete_finished_url=reverse('deletefinished')
    self.kitchen_delete_all_url=reverse('deleteall')

    self.shopping_url=reverse('shopping')
    self.shopping_addToBuy_url=reverse('add_to_buy')
    self.shopping_done_url=reverse('done')


  def test_singup_view(self):
    response = self.client.get(self.signup_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'signup.html')

  def test_home_view(self):
    response = self.client.get(self.home_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'home.html')

############################################################

  def test_products_view(self):
    response = self.client.get(self.products_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'products.html')

  def test_recipes_view(self):
    response = self.client.get(self.recipes_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'recipes.html')

###########################################################

  def test_shopping_view(self):
    response = self.client.get(self.shopping_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'shopping.html')


  def test_shopping_addToBuy_view(self):
    response = self.client.get(self.shopping_url,data={'text':'abcd'})
    self.client.post(self.shopping_addToBuy_url, data={'text':'abcd'})


    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'shopping.html')
    #self.assertRedirects(response, self.shopping_url, 200, 200)
    #print(response.context['form'].initial['text'])
    #self.assertEqual(response.context['form'].initial['text'], 'abcd')
    #self.assertEquals(response.status_code, 302)
  
  def test_shopping_done_view(self):
    response = self.client.get(self.shopping_url)
    self.client.post(self.shopping_done_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'shopping.html')
    #self.assertRedirects(response, self.shopping_url, 200, 200)


       
###############################################################3

  def test_kitchen_view(self):
    response = self.client.get(self.kitchen_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'kitchen.html')

"""
  def test_kitchen_add_view(self):
    response = self.client.get(self.kitchen_add_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'kitchen.html')

  def test_kitchen_finished_view(self):
    response = self.client.get(self.kitchen_finished_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'kitchen.html')

  def test_kitchen_deletefinished_view(self):
    response = self.client.get(self.delete_finished_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'kitchen.html')

  def test_kitchen_deleteALL_view(self):
    response = self.client.get(self.delete_all_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'kitchen.html')
"""
###############################################################
