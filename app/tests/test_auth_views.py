from django.test import TestCase
from django.urls import reverse

from app.forms.auth import CustomUserCreationForm
from app.models import PurBeurreUser


class HomepageTest(TestCase):
    @classmethod
    def setUp(cls):
        user = PurBeurreUser.objects.create_user("example@example.com", "password")
        user.save()

    def test_login_view_url_exists_at_desired_location(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_view_url_accessible_by_name(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_register_view_url_exists_at_desired_location(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)

    def test_register_view_url_accessible_by_name(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_logout_view_url_exists_at_desired_location(self):
        self.client.login(username="example@example.com", password="password")
        response = self.client.get("/logout/")
        self.assertRedirects(response, reverse("index"))

    def test_logout_view_url_accessible_by_name(self):
        self.client.login(username="example@example.com", password="password")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("index"))

    def test_my_account_view_url_exists_at_desired_location(self):
        self.client.login(username="example@example.com", password="password")
        response = self.client.get("/my-account/")
        self.assertEqual(response.status_code, 200)

    def test_my_account_view_url_accessible_by_name(self):
        self.client.login(username="example@example.com", password="password")
        response = self.client.get(reverse("my_account"))
        self.assertEqual(response.status_code, 200)

    def test_post_register(self):
        register_form = CustomUserCreationForm(data={
            "email": "example.example@example.com",
            "password1": "pexoyeH9B@!t-aChastU",
            "password2": "pexoyeH9B@!t-aChastU"
        })
        self.assertTrue(register_form.is_valid())
        response = self.client.post(reverse("register"), register_form.data)
        self.assertRedirects(response, reverse("index"))
