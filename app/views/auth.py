from django.contrib.auth import login as django_login, logout as django_logout
from django.shortcuts import render, redirect

from app.forms.auth import CustomUserCreationForm
from app.forms.search import SearchForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()

    return render(request, "app/register.html", {
        "register_form": form,
        "search_form": SearchForm()
    })


def logout(request):
    django_logout(request)
    return redirect("index")


def my_account(request):
    return render(request, "app/my_account.html")
