import datetime

import requests
from tqdm import tqdm
from django.core.management import BaseCommand

from app.models import Category, Product, CategoryProduct


class Command(BaseCommand):

    def handle(self, *args, **options):
        time_beginning = datetime.datetime.now()

        print("Cleaning the database...")

        CategoryProduct.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

        print("Cleaning done!")

        print("Downloading products...")

        url = "https://fr.openfoodfacts.org/categories.json"
        request = requests.get(url)

        all_categories = request.json()["tags"]
        good_categories = [category for category in all_categories if category["products"] >= 5000]

        for category in tqdm(good_categories):
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
                    "nutriments",
                    "nutrition_grade_fr",
                    "image_front_url",
                    "quantity"
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
                                code=product["code"],
                                name=product["product_name"],
                                quantity=product["quantity"],
                                nutrition_score=nutriments["nutrition-score-fr"],
                                nutrition_grade=product["nutrition_grade_fr"],
                                energy_100g=nutriments["energy_value"],
                                energy_unit=nutriments["energy_unit"],
                                carbohydrates_100g=nutriments["carbohydrates_100g"],
                                sugars_100g=nutriments["sugars_100g"],
                                fat_100g=nutriments["fat_100g"],
                                saturated_fat_100g=nutriments["saturated-fat_100g"],
                                salt_100g=nutriments["salt_100g"],
                                sodium_100g=nutriments["sodium_100g"],
                                fiber_100g=nutriments["fiber_100g"],
                                proteins_100g=nutriments["proteins_100g"],
                                thumbnail_url=product["image_front_url"]
                            )

                            CategoryProduct.objects.create(category_id=db_category.code, product_id=food.code)

                            print("Product saved successfully !")

                        else:
                            print("Not OK, nutriments missing")
                    else:
                        print("Not OK, product properties missing")

        print("Download done!")

        time_ending = datetime.datetime.now()

        print(f"Operation duration : {time_ending - time_beginning}")
