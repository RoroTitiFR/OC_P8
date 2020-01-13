from django.db import models


class Product(models.Model):
    code = models.TextField(primary_key=True)
    name = models.TextField()

    nutrition_score = models.IntegerField()
    nutrition_grade = models.CharField(max_length=1)

    energy_100g = models.IntegerField()
    energy_unit = models.TextField()
    carbohydrates_100g = models.FloatField()
    sugars_100g = models.FloatField()
    fat_100g = models.FloatField()
    saturated_fat_100g = models.FloatField()
    salt_100g = models.FloatField()
    sodium_100g = models.FloatField()
    fiber_100g = models.FloatField()
    proteins_100g = models.FloatField()

    thumbnail_url = models.TextField()


class Category(models.Model):
    code = models.TextField(primary_key=True)
    name = models.TextField()


class CategoryProduct(models.Model):
    class Meta:
        unique_together = [['category', 'product']]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
