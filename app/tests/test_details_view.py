from django.test import TestCase
from django.urls import reverse

from app.models import Product


class TestDetailsView(TestCase):
    @classmethod
    def setUp(cls):
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
        response = self.client.get("/details/1/")
        self.assertEqual(response.status_code, 200)

    # TODO
    # def test_details_view_redirects_if_code_none(self):
    #     response = self.client.get("/details/")
    #     self.assertRedirects(response, reverse("index"))

    # TODO
    # def test_details_view_redirects_if_code_does_not_exist(self):
    #     response = self.client.get("/details/10/")
    #     self.assertRedirects(response, reverse("index"))

    def test_substitutes_view_url_accessible_by_name(self):
        response = self.client.get(reverse("details", kwargs={"code": "5"}))
        self.assertEqual(response.status_code, 200)

    def test_substitutes_view_uses_correct_template(self):
        response = self.client.get(reverse("details", kwargs={"code": "5"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/details.html")
