from django.test import TestCase
from django.urls import reverse

from app.models import Product


class TestDetailsView(TestCase):
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

    def test_details_view_url_exists_at_desired_location(self):
        """Test the product details view URL exists
        """
        response = self.client.get("/details/1/")
        self.assertEqual(response.status_code, 200)

    def test_details_view_404_if_code_none(self):
        """Test the product details view returns 404 when no product code provided
        """
        response = self.client.get("/details/")
        self.assertEqual(response.status_code, 404)

    def test_details_view_show_error_if_code_does_not_exist(self):
        """Test the product details view shows an error if the product code is wrong
        """
        response = self.client.get(reverse("details", kwargs={"code": "10"}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("error_message", response.context)
        self.assertTemplateUsed(response, "app/error.html")
