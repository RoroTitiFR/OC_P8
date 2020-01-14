from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from app.models import PurBeurreUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = PurBeurreUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = PurBeurreUser
        fields = ('email',)
