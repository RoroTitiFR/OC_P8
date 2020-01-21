from django.test import TestCase

from app.forms.search_product import SearchProductForm


class YourTestClass(TestCase):
    def test_search_product_form_with_valid_data(self):
        register_form = SearchProductForm(data={
            "search_term": "product"
        })
        self.assertTrue(register_form.is_valid())

    def test_search_product_form_with_invalid_data(self):
        register_form = SearchProductForm(data={
            "search_term": None
        })
        self.assertFalse(register_form.is_valid())
