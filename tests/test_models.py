from django.test import TestCase
from kitchen.models import Products
from products.models import Product
from shopping.models import ToBuy
from recipes.models import Recipe,ProductInRecipe


class TestModels(TestCase):

    def setUp(self):
        self.product1=Product.objects.create(name="milk")
        self.kitchen_product1=Products.objects.create(product=self.product1,quantity=10,unit="l")
        self.shopping_product1=ToBuy.objects.create(product=self.product1,quantity=10,unit="l")
        self.recipe1=Recipe.objects.create(title="cake",directions="aaaaaa")
        self.product_in_recipe1=ProductInRecipe.objects.create(product=self.product1,recipe=self.recipe1,quantity=10,unit='l')

    
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