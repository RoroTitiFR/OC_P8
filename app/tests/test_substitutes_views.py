from django.test import TestCase
from django.urls import reverse

from app.models import Product, UserProduct, PurBeurreUser, Category, CategoryProduct


class HomepageTest(TestCase):
    @classmethod
    def setUp(cls):
        category = Category.objects.create(
            code=1,
            name="My category"
        )

        for index in range(1, 5 + 1):
            product = Product.objects.create(
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

            CategoryProduct.objects.create(
                category_id=category.code,
                product_id=product.code
            )

        user = PurBeurreUser.objects.create_user("example@example.com", "password")

        UserProduct.objects.create(user_id=user.id, product_id="5", substitute_id="1")

    def test_substitutes_view_url_exists_at_desired_location(self):
        response = self.client.get("/substitutes/5/")
        self.assertEqual(response.status_code, 200)

    def test_substitutes_view_redirects_if_code_none(self):
        response = self.client.get("/substitutes/")
        self.assertRedirects(response, reverse("index"))

    def test_substitutes_view_redirects_if_code_does_not_exist(self):
        response = self.client.get("/substitutes/10/")
        self.assertRedirects(response, reverse("index"))

    def test_substitutes_view_url_accessible_by_name(self):
        response = self.client.get(reverse("substitutes", kwargs={"code": "5"}))
        self.assertEqual(response.status_code, 200)

    def test_substitutes_view_uses_correct_template(self):
        self.client.login(username="example@example.com", password="password")
        response = self.client.get(reverse("substitutes", kwargs={"code": "5"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["substitutes"]), 4)
        self.assertTrue(response.context["substitutes"][0].saved)
        self.assertTemplateUsed(response, "app/substitutes.html")
        self.assertTemplateUsed(response, "app/layout.html")
        self.assertTemplateUsed(response, "app/navbar.html")

    def test_delete_substitute_view(self):
        self.client.login(username="example@example.com", password="password")
        couple = UserProduct.objects.first()
        response = self.client.get(reverse("delete_substitute", kwargs={"couple_id": couple.id}))
        self.assertRedirects(response, reverse("my_substitutes"))
        self.assertEqual(len(UserProduct.objects.all()), 0)

    def test_substitutes_view_posting_form(self):
        data = {
            "product_code": 1,
            "substitute_code": 2
        }

        self.client.login(username="example@example.com", password="password")
        response = self.client.post(reverse("substitutes"), data)
        self.assertTemplateUsed(response, "app/saved_indicator.html")
        self.assertEqual(UserProduct.objects.get(substitute_id="2").product.code, "1")
        self.assertEqual(UserProduct.objects.get(substitute_id="2").substitute.code, "2")
