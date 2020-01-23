from django.test import TestCase
from django.urls import reverse

from app.models import Product


class TestSearchProduct(TestCase):
    search_one_product_kwargs = {"search_term": "product 2"}
    search_multiple_products_kwargs = {"search_term": "product"}
    search_no_product_kwargs = {"search_term": "xyz"}

    @classmethod
    def setUp(cls):
        """Creating a testing context
        """
        for index in range(1, 5 + 1):
            Product.objects.create(
                code=index,
                name=f"My product {index}",
                nutrition_score=index,
                nutrition_grade="a",
                quantity=f"{index}00 g",
                energy_100g=0,
                energy_unit="kcal",
                carbohydrates_100g=0,
                sugars_100g=0,
                fat_100g=0,
                saturated_fat_100g=0,
                salt_100g=0,
                sodium_100g=0,
                fiber_100g=0,
                proteins_100g=0,
                thumbnail_url="example.com"
            )

    def test_search_product_view_url_exists_at_desired_location(self):
        """Test the search product view URL exists
        """
        response = self.client.get("/results/product 2/")
        self.assertEqual(response.status_code, 200)

    def test_search_product_view_url_redirects_if_product_none(self):
        """Test the search product view redirects to index when no product code provided
        """
        response = self.client.get("/results/")
        self.assertRedirects(response, reverse("index"))

    def test_search_product_view_url_accessible_by_name(self):
        """Test the search product view URL is accessible by name
        """
        response = self.client.get(reverse("results", kwargs=self.search_one_product_kwargs))
        self.assertEqual(response.status_code, 200)

    def test_search_product_view_uses_correct_template(self):
        """Test the search product view uses the correct template
        """
        response = self.client.get(reverse("results", kwargs=self.search_one_product_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/search_results.html")
        self.assertTemplateUsed(response, "app/layout.html")
        self.assertTemplateUsed(response, "app/navbar.html")

    def test_search_product_view_has_correct_no_product_found_search_result(self):
        """Test the search product view has correct comportment when no product found
        """
        response = self.client.get(reverse("results", kwargs=self.search_no_product_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["products"]), 0)

    def test_search_product_view_has_correct_one_search_result(self):
        """Test the search product view has correct result when one result expected
        """
        response = self.client.get(reverse("results", kwargs=self.search_one_product_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["products"]), 1)
        self.assertEqual(response.context["products"][0].code, "2")

    def test_search_product_view_has_correct_multiple_search_results(self):
        """Test the search product view has correct result when multiple results expected
        """
        response = self.client.get(reverse("results", kwargs=self.search_multiple_products_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["products"]), 5)
