from django.test import SimpleTestCase
from kitchen.forms import ProductsForm


class TestForms(SimpleTestCase):

    def test_kitchen_ProductsForm_valid_data(self):
        form= ProductsForm(data={
            'text':'milk',
            'amount':'l'
        })

        self.assertTrue(form.is_valid())

    def test_kitchen_ProductsForm_no_data(self):
        form= ProductsForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),2)