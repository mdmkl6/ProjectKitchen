from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import login
from kitchen.models import Products
from products.models import Product
from shopping.models import ToBuy
from recipes.models import Recipe,ProductInRecipe,UserRating


class TestModels(TestCase):

    def setUp(self):
        user = User.objects.create(username='user1')
        user.set_password('haslo1234')
        user.save() 
        self.client=Client()
        self.client.login(username='user1', password='haslo1234')

        self.product1=Product.objects.create(name="milk")
        self.kitchen_product1=Products.objects.create(product=self.product1,quantity=10,unit="l",finished=False,owner=user)
        self.shopping_product1=ToBuy.objects.create(product=self.product1,quantity=10,unit="l",owner=user)
        self.recipe1=Recipe.objects.create(title="cake",directions="aaaaaa")
        self.product_in_recipe1=ProductInRecipe.objects.create(product=self.product1,recipe=self.recipe1,quantity=10,unit='l')
        self.recipes_UserRating=UserRating.objects.create(recipe=self.recipe1,score=5,owner=user)
    
    def test_Product_str(self):
        self.assertEquals(str(self.product1),"milk")

    def test_kitchen_product_str(self):
        self.assertEquals(str(self.kitchen_product1),"milk")

    def test_schopping_product_str(self):
        self.assertEquals(str(self.shopping_product1),"milk")
    
    def test_recipe_str(self):
        self.assertEquals(str(self.recipe1),"cake")

    def test_product_in_recipe_str(self):
        self.assertEquals(str(self.product_in_recipe1),"milk")

    def test_recipes_UserRating_str(self):
        self.assertEquals(str(self.recipes_UserRating),"user1 rating 5 for cake")