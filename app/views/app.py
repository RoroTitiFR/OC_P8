from typing import List
from urllib.parse import quote

import jellyfish as jellyfish
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from app.forms.delete_saved_substitute_form import DeleteSavedSubstituteForm
from app.forms.save_substitute import SaveSubstituteForm
from app.forms.search import SearchForm
from app.models import Product, CategoryProduct, Category, UserProduct


def index(request):
    """The index view, showing the homepage and handling search product requests
    :param request: provided by Django
    """
    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            return redirect(reverse("results", kwargs={"search_term": quote(form.data["search_term"])}))

    else:
        form = SearchForm()

    return render(request, "app/index.html", {
        "search_form": form
    })


def results(request, search_term=""):
    """The search results view, showing the search results
    :param request: provided by Django
    :param search_term: the term to search for into the database
    """
    if search_term == "":
        return redirect(reverse("index"))

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
    """The find substitutes view, showing the possible substitutes for a given product and handling save substitute requests
    :param request: provided by Django
    :param code: The code of the product against which searching for substitutes
    """
    if request.POST:
        form = SaveSubstituteForm(request.POST)

        if form.is_valid():
            product_code = form.cleaned_data["product_code"]
            substitute_code = form.cleaned_data["substitute_code"]

            user_product = UserProduct(user_id=request.user.id, product_id=product_code, substitute_id=substitute_code)
            user_product.save()

            return render(request, "app/saved_indicator.html")

    else:
        if code == "":
            return redirect(reverse("index"))

        try:
            search_product: Product = Product.objects.get(code=code)
        except Product.DoesNotExist:
            return redirect(reverse("index"))

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
    """The details view, computing the product details modal content
    :param request: provided by Django
    :param code: the code of the product for which we want the details
    """
    try:
        product = Product.objects.get(code=code)
    except Product.DoesNotExist:
        return render(request, "app/error.html", {
            "error_message": "Ce produit n'existe pas dans la base de données."
        })

    return render(request, "app/details.html", {
        "product": product
    })


@login_required
def my_substitutes(request):
    """The saved substitutes view, displaying the substitutes saved by the user and handling deletion requests
    :param request: provided by Django
    """
    if request.POST:
        form = DeleteSavedSubstituteForm(request.POST)

        if form.is_valid():
            product_substitute_id = form.cleaned_data["product_substitute_id"]

            user_id = request.user.id
            UserProduct.objects.get(id=product_substitute_id, user_id=user_id).delete()
            return redirect(reverse("my_substitutes"))

    else:
        user_id = request.user.id
        saved_substitutes = UserProduct.objects.filter(user_id=user_id)

        return render(request, "app/saved_substitutes.html", {
            "substitutes": saved_substitutes,
            "search_form": SearchForm()
        })


def compute_similarities(products, search_term):
    """Compute the similarity property of each product of the list, compared to a given search term
    :param products: the products list to process
    :param search_term: the search term to which we will compare the products names
    """
    for product in products:
        product.similarity = round_by_hundred(jellyfish.jaro_distance(product.name, search_term) * 1000)

    return products


def round_by_hundred(number):
    """Round a number by 100
    :param number: the number to be rounded
    :return: the rounded value
    """
    return int(round(number / 100)) * 100
