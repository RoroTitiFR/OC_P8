from urllib.parse import quote

import requests
from django.shortcuts import render, redirect

from app.forms.search import SearchForm

expected_product_keys = [
    "image_front_url",
    "product_name",
    "code",
    "quantity",
    "compared_to_category"
]


def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            return redirect("/results/" + quote(form.data["search_term"]))

    else:
        form = SearchForm()

    return render(request, "app/home.html", {
        "form": form
    })


def results(request, search_term=""):
    if search_term == "":
        return redirect("/")

    request_url = "https://fr.openfoodfacts.org/cgi/search.pl?" \
                  "action=process&" \
                  f"search_terms={search_term}&" \
                  "sort_by=unique_scans_n&" \
                  "page_size=20&" \
                  "action=display&" \
                  "json=1"

    r = requests.get(request_url)
    json = r.json()

    products = []

    for product in json["products"]:
        # Check if the required keys exists
        if all(key in product for key in expected_product_keys):
            # Check if all the keys contain a value
            if all(product[key] for key in expected_product_keys):
                product["product_name"] = get_display_name_for_product(product)
                products.append(product)

    form = SearchForm()

    return render(request, "app/search_results.html", {
        "products": products,
        "form": form,
        "search_term": search_term
    })


def substitutes(request, code=0):
    if code == 0:
        return redirect("/")

    request_url = f"https://fr.openfoodfacts.org/api/v0/product/{code}.json"
    result = requests.get(request_url)

    if "product" in result.json():
        search_product = result.json()["product"]
        search_product["product_name"] = get_display_name_for_product(search_product)
    else:
        return redirect("/")

    # Check if the required keys exists, and that the keys contain a value
    if all(key in search_product for key in expected_product_keys) and all(search_product[key] for key in expected_product_keys):
        category = search_product["compared_to_category"]

        # Now let's search other products from the same category
        request_url = ("https://fr.openfoodfacts.org/cgi/search.pl?"
                       "action=process&"
                       "tagtype_0=categories&"
                       "tag_contains_0=contains&"
                       f"tag_0={category}&"
                       "sort_by=unique_scans_n&"
                       "page_size=50&"
                       "json=1")

        products = requests.get(request_url).json()["products"]

        good_products = []

        for product in products:
            if all(key in product for key in expected_product_keys) and all(product[key] for key in expected_product_keys):
                product["product_name"] = get_display_name_for_product(product)
                good_products.append(product)

    else:
        return redirect("/")

    form = SearchForm()

    return render(request, "app/substitutes.html", {
        "form": form,
        "products": good_products,
        "product": search_product
    })


def get_display_name_for_product(product):
    return product["product_name"] + ", " + product["quantity"]
