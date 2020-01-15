from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from app.forms.auth import CustomUserCreationForm, LoginForm
from app.forms.search import SearchForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()

    return render(request, "app/signup.html", {
        "signup_form": form,
        "search_form": SearchForm()
    })
