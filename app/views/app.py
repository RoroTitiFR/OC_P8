from typing import List
from urllib.parse import quote

import jellyfish as jellyfish
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app.forms.save_substitute import SaveSubstituteForm
from app.forms.search import SearchForm
from app.models import Product, CategoryProduct, Category, UserProduct


def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            return redirect("/results/" + quote(form.data["search_term"]))

    else:
        form = SearchForm()

    return render(request, "app/home.html", {
        "search_form": form
    })


def results(request, search_term=""):
    if search_term == "":
        return redirect("/")

    products = Product.objects.filter(name__icontains=search_term)

    # Computing the similarity property into the product object
    products = compute_similarities(products, search_term)

    # Finding the best similarity level to obtain at least 1 good result
    current_similarity_threshold = 1000
    good_results = []

    while True:
        if current_similarity_threshold == 0:
            break

        good_results = [result for result in products if result.similarity >= current_similarity_threshold]

        if len(good_results) > 0:
            good_results = sorted(good_results, key=lambda x: x.nutrition_score)
            break
        else:
            current_similarity_threshold -= 100

    return render(request, "app/search_results.html", {
        "products": good_results,
        "search_form": SearchForm(),
        "search_term": search_term
    })


def substitutes(request, code=""):
    if request.POST:
        form = SaveSubstituteForm(request.POST)
        print(request.user.id)

        if form.is_valid():
            product_code = form.cleaned_data["product_code"]
            substitute_code = form.cleaned_data["substitute_code"]

            user_product = UserProduct(user_id=request.user.id, product_id=product_code, substitute_id=substitute_code)
            user_product.save()

            return render(request, "app/saved_indicator.html")

    else:
        if code == "":
            return redirect("/")

        search_product: Product = Product.objects.get(code=code)

        if not search_product:
            return redirect("/")

        # Finding all the categories of the product
        category_products: List[CategoryProduct] = CategoryProduct.objects.filter(product_id=search_product.code)

        # Finding the code of the category which counts the least items
        smallest_category = None
        smallest_count = 0

        for category_product in category_products:
            if smallest_count == 0 or Category.objects.filter(code=category_product.category_id).count() < smallest_count:
                smallest_count = Category.objects.filter(code=category_product.category_id).count()
                smallest_category = category_product.category

        # Finding substitutes in selected category
        products_ids = CategoryProduct.objects.filter(category=smallest_category).values_list("product_id", flat=True)
        products = Product.objects.filter(code__in=products_ids)

        # Computing the similarity property into the product object
        products = compute_similarities(products, search_product.name)

        # Finding the best similarity level to obtain at least 1 good result
        current_similarity_threshold = 1000
        good_substitutes = []

        while True:
            if current_similarity_threshold == 0:
                break

            possible_substitutes: List[Product] = [result for result in products
                                                   if result.similarity >= current_similarity_threshold]

            possible_substitutes = [possible_substitute for possible_substitute in possible_substitutes
                                    if possible_substitute.code != search_product.code]

            good_substitutes = [possible_substitute for possible_substitute in possible_substitutes
                                if possible_substitute.nutrition_score < search_product.nutrition_score]

            if len(good_substitutes) > 0:
                good_substitutes = sorted(good_substitutes, key=lambda x: x.nutrition_score)
                break
            else:
                current_similarity_threshold -= 100

        saved_substitutes = UserProduct.objects.filter(user_id=request.user.id, product_id=code).values_list("substitute_id", flat=True)

        for substitute in good_substitutes:
            if substitute.code in saved_substitutes:
                substitute.saved = True

        return render(request, "app/substitutes.html", {
            "search_form": SearchForm(),
            "substitutes": good_substitutes,
            "product": search_product
        })


def details(request, code):
    product = Product.objects.get(code=code)

    return render(request, "app/details.html", {
        "product": product
    })


@login_required
def my_substitutes(request):
    user_id = request.user.id
    saved_substitutes = UserProduct.objects.all()

    return render(request, "app/saved_substitutes.html", {
        "substitutes": saved_substitutes
    })


def compute_similarities(products, search_term):
    for product in products:
        product.similarity = round_by_hundred(jellyfish.jaro_distance(product.name, search_term) * 1000)

    return products


def round_by_hundred(n: float) -> int:
    """
    Round a number by 100

    :param n: The number to be rounded
    :return: The rounded value
    """
    return int(round(n / 100)) * 100
