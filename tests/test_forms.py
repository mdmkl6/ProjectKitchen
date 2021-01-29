from django.test import SimpleTestCase
from kitchen.forms import ProductInKitchenForm


class TestForms(SimpleTestCase):

    def test_kitchen_ProductInKitchenForm_valid_data(self):
        form= ProductInKitchenForm(data={
            'text':'milk',
            'amount':'l'
        })

        self.assertTrue(form.is_valid())

    def test_kitchen_ProductInKitchenForm_no_data(self):
        form= ProductInKitchenForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),2)