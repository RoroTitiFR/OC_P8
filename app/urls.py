from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("results/", views.results, name="results"),
    path("results/<str:search_term>/", views.results, name="results"),
    path("substitutes/", views.substitutes, name="substitutes"),
    path("substitutes/<str:code>/", views.substitutes, name="substitutes")
]
