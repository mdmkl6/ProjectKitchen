from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login
from shopping.forms import ToBuyForm
from recipes.models import Recipe, UserRating
from products.models import Product
from kitchen.models import Products


class TestViews(TestCase):

  def setUp(self):
    user = User.objects.create(username='user1')
    user.set_password('haslo1234')
    user.save() 
    self.client=Client()
    self.client.login(username='user1', password='haslo1234')

    recipe1=Recipe.objects.create(title="cake",directions="make")
    recipe2=Recipe.objects.create(title="cake2",directions="make")
    product1=Product.objects.create(name="milk")
    kitchen1=Products.objects.create(product=product1,quantity=1,unit='l',finished=False,owner=user)

    self.home_url=reverse('home')
    self.signup_url=reverse('signup')

    self.products_url=reverse('products')

    self.recipes_url=reverse('recipes')
    self.single_recipes_url=reverse('recipe',kwargs={'id':recipe1.id})
    self.recipes_user_rating_url=reverse('user_rating',kwargs={'id':recipe1.id})

    self.kitchen_url=reverse('kitchen')
    self.kitchen_add_url=reverse('add')
    self.kitchen_finished_url=reverse('finished',kwargs={'kitchen_id':kitchen1.pk})
    self.kitchen_delete_finished_url=reverse('deletefinished')
    self.kitchen_delete_all_url=reverse('deleteall')
    self.kitchen_autocomplete_kitchen_url=reverse('autocomplete_kitchen')
    self.kitchen_change_amount_url=reverse('change_amount',kwargs={'product_id':product1.pk})

    self.shopping_url=reverse('shopping')
    self.shopping_addToBuy_url=reverse('add_to_buy')
    self.shopping_done_url=reverse('done')
    self.shopping_autocomplete_list_url=reverse('autocomplete_shopping_list')


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

###############################################################

  def test_recipes_view(self):
    response = self.client.get(self.recipes_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'recipes.html')

  def test_single_recipes_view(self):
    response = self.client.get(self.single_recipes_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'recipe.html')

  def test_recipes_user_rating_bad_view(self):
    response = self.client.get(self.recipes_user_rating_url)

    self.assertEquals(response.status_code, 200)
    self.assertJSONEqual(response.content,{'success': 'false'})

  def test_recipes_user_rating_view(self):
    response = self.client.post(self.recipes_user_rating_url, data={'rating_value':5})

    self.assertEquals(response.status_code, 200)
    self.assertJSONEqual(response.content,{'success': 'true','score':'5'})

###########################################################

  def test_shopping_view(self):
    response = self.client.get(self.shopping_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'shopping.html')


  def test_shopping_addToBuy_view(self):
    response = self.client.post(self.shopping_addToBuy_url, data={'text':'abcd'})
    self.assertRedirects(response, self.shopping_url)


  def test_shopping_done_view(self):
    response = self.client.post(self.shopping_done_url)
    self.assertRedirects(response, self.shopping_url)

  def test_shopping_autocomplete_list_view(self):
    response = self.client.get(self.shopping_autocomplete_list_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'shopping.html')

###############################################################

  def test_kitchen_view(self):
    response = self.client.get(self.kitchen_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'kitchen.html')


  def test_kitchen_add_view(self):
    response = self.client.post(self.kitchen_add_url, data={'text':'abcd'})
    self.assertRedirects(response, self.kitchen_url)


  def test_kitchen_finished_view(self):
    response = self.client.post(self.kitchen_finished_url)
    self.assertRedirects(response, self.kitchen_url)

  def test_kitchen_deletefinished_view(self):
    response = self.client.post(self.kitchen_delete_finished_url)
    self.assertRedirects(response, self.kitchen_url)

  def test_kitchen_deleteALL_view(self):
    response = self.client.post(self.kitchen_delete_all_url)
    self.assertRedirects(response, self.kitchen_url)

  def test_kitchen_autocomplete_view(self):
    response = self.client.get(self.kitchen_autocomplete_kitchen_url)
    
    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'kitchen.html')

  def test_kitchen_change_amount_view(self):
    response = self.client.post(self.kitchen_change_amount_url, data={'amount':'2l'})
    self.assertRedirects(response, self.kitchen_url)

###############################################################
