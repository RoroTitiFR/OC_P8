from urllib.parse import quote

import requests
from django.shortcuts import render, redirect

from app.forms.search import SearchForm


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
        if "image_front_url" in product and "product_name" in product and "quantity" in product:
            # Check if all the keys contain a value
            if product["image_front_url"] and product["product_name"] and product["quantity"]:
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

    form = SearchForm()

    return render(request, "app/substitutes.html", {
        "form": form,
        "code": code
    })
