from django.contrib.auth import views as auth_views
from django.urls import path

from app import views
from app.forms.auth import LoginForm
from app.forms.search import SearchForm

urlpatterns = [
    path("", views.index, name="index"),
    path("results/", views.results, name="results"),
    path("results/<str:search_term>/", views.results, name="results"),
    path("substitutes/", views.substitutes, name="substitutes"),
    path("substitutes/<str:code>/", views.substitutes, name="substitutes"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(
        template_name="app/login.html", authentication_form=LoginForm, extra_context={
            "search_form": SearchForm()
        }
    ), name="login"),
    path("logout/", views.logout, name="logout"),
    path("my-account/", views.my_account, name="my_account"),
    path("my-substitutes/", views.my_substitutes, name="my_substitutes"),
    path("details/<str:code>/", views.details, name="details"),
    path("legal/", views.legal, name="legal")
]
