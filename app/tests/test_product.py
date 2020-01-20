from django.test import TestCase

from app.models import Product


class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        product = Product.objects.create(
            name="My product",
            nutrition_score=0,
            nutrition_grade=0,
            quantity="300 g",
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
        self.assertEqual(product.display_name, "My product, 300 g")

    def test_kcal(self):
        product = Product.objects.first()
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
