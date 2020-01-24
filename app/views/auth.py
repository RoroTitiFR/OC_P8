from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from app.forms.auth import CustomUserCreationForm, CustomUserChangeForm
from app.forms.search import SearchForm


def register(request):
    """The register view, showing the register page and handling register requests
    :param request: provided by Django
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect(reverse("index"))
    else:
        form = CustomUserCreationForm()

    return render(request, "app/register.html", {
        "register_form": form,
        "search_form": SearchForm()
    })


@login_required
def logout(request):
    """The logout view, handling logout requests
    :param request: provided by Django
    """
    django_logout(request)
    return redirect(reverse("index"))


@login_required
def my_account(request):
    """The account settings view, showing the change email page and handling the change account email requests
    :param request:
    """
    if request.method == "POST":
        form = CustomUserChangeForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, "app/my_account.html", {
                "success": "Vos informations ont bien été mises à jour.",
                "change_form": form,
                "search_form": SearchForm()
            })
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, "app/my_account.html", {
        "change_form": form,
        "search_form": SearchForm()
    })
