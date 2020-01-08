from urllib.parse import quote

import requests
from django.http import HttpResponse
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

    form = SearchForm()

    return render(request, "app/search_results.html", {
        "json": json,
        "form": form
    })
