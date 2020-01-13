import requests
from django.core.management import BaseCommand

from app.models import Category, Product, CategoryProduct


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = "https://fr.openfoodfacts.org/categories.json"
        request = requests.get(url)

        categories = request.json()["tags"]

        for category in categories:
            if category["products"] >= 5000:

                db_category = Category(code=category["id"], name=category["name"])
                db_category.save()

                url = ("https://fr.openfoodfacts.org/cgi/search.pl?"
                       "action=process&"
                       "tagtype_0=categories&"
                       "tag_contains_0=contains&"
                       f"tag_0={category['id']}&"
                       "sort_by=unique_scans_n&"
                       "page_size=50&"
                       "json=1")

                request = requests.get(url)

                expected_product_keys = [
                    "product_name",
                    "code",
                    "allergens_from_ingredients",
                    "nutriments",
                    "nutrition_grade_fr",
                ]

                expected_nutriments_keys = [
                    "nutrition-score-fr",
                    "energy_value",
                    "energy_unit",
                    "carbohydrates_100g",
                    "sugars_100g",
                    "saturated-fat_100g",
                    "sodium_100g",
                    "salt_100g",
                    "fiber_100g",
                    "proteins_100g"
                ]

                for product in request.json()["products"]:
                    if all(key in product for key in expected_product_keys):
                        nutriments = product["nutriments"]
                        if all(key in nutriments for key in expected_nutriments_keys):
                            # The product has all required characteristics to be integrated into the database
                            print("Product OK")

                            # Inserting the food product into the database
                            food, created = Product.objects.get_or_create(
                                carbohydrates_100g=nutriments["carbohydrates_100g"],
                                energy_100g=nutriments["energy_value"],
                                energy_unit=nutriments["energy_unit"],
                                fat_100g=nutriments["fat_100g"],
                                fiber_100g=nutriments["fiber_100g"],
                                code=product["code"],
                                name=product["product_name"],
                                nutrition_score=nutriments["nutrition-score-fr"],
                                nutrition_grade=product["nutrition_grade_fr"],
                                proteins_100g=nutriments["proteins_100g"],
                                salt_100g=nutriments["salt_100g"],
                                saturated_fat_100g=nutriments["saturated-fat_100g"],
                                sodium_100g=nutriments["sodium_100g"],
                                sugars_100g=nutriments["sugars_100g"]
                            )

                            CategoryProduct.objects.create(category_id=db_category.code, product_id=food.code)

                            print("Product saved successfully !")

                        else:
                            print("Not OK, nutriments missing")
                    else:
                        print("Not OK, product properties missing")
