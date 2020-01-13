from urllib.parse import quote

from django.shortcuts import render, redirect

from app.forms.search import SearchForm
from app.models import Product


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

    products = Product.objects.filter(name__icontains=search_term)

    form = SearchForm()

    return render(request, "app/search_results.html", {
        "products": products,
        "form": form,
        "search_term": search_term
    })


def substitutes(request, code=0):
    if code == 0:
        return redirect("/")

    result = Product.objects.filter(code=code)

    if result:
        search_product = result
    else:
        return redirect("/")

    category = search_product["compared_to_category"]

    # TODO : code to find substitutes
    # # Now let's search other products from the same category
    # request_url = ("https://fr.openfoodfacts.org/cgi/search.pl?"
    #                "action=process&"
    #                "tagtype_0=categories&"
    #                "tag_contains_0=contains&"
    #                f"tag_0={category}&"
    #                "sort_by=unique_scans_n&"
    #                "page_size=50&"
    #                "json=1")
    #
    # products = requests.get(request_url).json()["products"]
    #
    # good_products = []
    #
    # for product in products:
    #     if all(key in product for key in expected_product_keys) and all(product[key] for key in expected_product_keys):
    #         product["product_name"] = get_display_name_for_product(product)
    #         good_products.append(product)

    form = SearchForm()

    return render(request, "app/substitutes.html", {
        "form": form,
        "products": good_products,
        "product": search_product
    })
