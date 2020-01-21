from django.test import TestCase

from app.models import Product


class YourTestClass(TestCase):
    product_name = "My product"
    product_quantity = "300 g"

    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            name=cls.product_name,
            nutrition_score=0,
            nutrition_grade="a",
            quantity=cls.product_quantity,
            energy_100g=8.368,
            energy_unit="kj",
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

    def test_display_name(self):
        product = Product.objects.first()
        self.assertEqual(product.display_name, f"{self.product_name}, {self.product_quantity}")

    def test_kcal_from_kj(self):
        product = Product.objects.first()
        self.assertEqual(product.kcal, 2)

    def test_kcal_from_kcal(self):
        product = Product.objects.first()
        product.energy_100g = 2
        product.energy_unit = "kcal"
        self.assertEqual(product.kcal, 2)

    def test_similarity(self):
        product = Product.objects.first()
        similarity = 500
        product.similarity = similarity
        self.assertEqual(product.similarity, similarity)

    def test_saved(self):
        product = Product.objects.first()
        self.assertFalse(product.saved)
        product.saved = True
        self.assertTrue(product.saved)
