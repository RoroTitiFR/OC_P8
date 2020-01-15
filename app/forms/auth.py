from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from app.models import PurBeurreUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Votre adresse mail",
            "class": "input"
        }),
        error_messages={
            "unique": "Un utilisateur avec cette adresse mail est déjà enregistré."
        }
    )

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Votre mot de passe",
            "class": "input"
        })
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirmez votre mot de passe",
            "class": "input"
        })
    )

    def is_valid(self):
        # noinspection PyCallByClass
        is_valid = forms.Form.is_valid(self)

        for error in self.errors:
            self.fields[error].widget.attrs.update({
                "class": self.fields[error].widget.attrs["class"] + " is-danger"
            })

        return is_valid

    class Meta:
        model = PurBeurreUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = PurBeurreUser
        fields = ("email",)


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Votre adresse mail",
            "class": "input"
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Votre mot de passe",
            "class": "input"
        })
    )
