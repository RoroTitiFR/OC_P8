from django.contrib.auth import login
from django.shortcuts import render, redirect

from app.forms.auth import CustomUserCreationForm


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()

    return render(request, "app/signup.html", {
        "form": form
    })
