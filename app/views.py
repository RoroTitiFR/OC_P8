from datetime import datetime

from django.shortcuts import render


def index(request):
    return render(request, "app/index.html", {
        "date": datetime.now()
    })
