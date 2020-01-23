from django.test import TestCase
from django.urls import reverse

from app.models import PurBeurreUser


class TestAuthViews(TestCase):
    @classmethod
    def setUp(cls):
        """Creating a testing context
        """
        PurBeurreUser.objects.create_user("example@example.com", "password")

    def test_login_view_url_exists_at_desired_location(self):
        """Test the login URL exists
        """
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_view_url_accessible_by_name(self):
        """Test the login URL is accessible by name
        """
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_view_uses_correct_template(self):
        """Test the login view uses the correct template
        """
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "app/login.html")
        self.assertTemplateUsed(response, "app/layout.html")
        self.assertTemplateUsed(response, "app/navbar.html")

    def test_register_view_url_exists_at_desired_location(self):
        """Test the register URL exists
        """
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)

    def test_register_view_url_accessible_by_name(self):
        """Test the register view URL is accessible by name
        """
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_view_uses_correct_template(self):
        """Test the register view uses the correct template
        """
        response = self.client.get(reverse("register"))
        self.assertTemplateUsed(response, "app/register.html")
        self.assertTemplateUsed(response, "app/layout.html")
        self.assertTemplateUsed(response, "app/navbar.html")

    def test_logout_view_url_exists_at_desired_location(self):
        """Test the logout view URL exists
        """
        self.client.login(username="example@example.com", password="password")
        response = self.client.get("/logout/")
        self.assertRedirects(response, reverse("index"))

    def test_logout_view_url_accessible_by_name(self):
        """Test the logout view URL is accessible by name
        """
        self.client.login(username="example@example.com", password="password")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("index"))

    def test_my_account_view_url_exists_at_desired_location(self):
        """Test the account admin view URL exists
        """
        self.client.login(username="example@example.com", password="password")
        response = self.client.get("/my-account/")
        self.assertEqual(response.status_code, 200)

    def test_my_account_view_url_accessible_by_name(self):
        """Test the account admin view URL is accessible by name
        """
        self.client.login(username="example@example.com", password="password")
        response = self.client.get(reverse("my_account"))
        self.assertEqual(response.status_code, 200)

    def test_my_account_view_uses_correct_template(self):
        """Test the account admin view uses the correct template
        """
        self.client.login(username="example@example.com", password="password")
        response = self.client.get(reverse("my_account"))
        self.assertTemplateUsed(response, "app/my_account.html")
        self.assertTemplateUsed(response, "app/layout.html")
        self.assertTemplateUsed(response, "app/navbar.html")

    def test_register_view_posting_form(self):
        """Test the register form with POST request
        """
        data = {
            "email": "example.example@example.com",
            "password1": "pexoyeH9B@!t-aChastU",
            "password2": "pexoyeH9B@!t-aChastU"
        }
        response = self.client.post(reverse("register"), data)
        self.assertRedirects(response, reverse("index"))
        self.assertEqual(PurBeurreUser.objects.count(), 2)

    def test_my_account_view_posting_form(self):
        """Test the change email form with POST request
        """
        data = {
            "email": "example.example.example@example.com"
        }
        self.client.login(username="example@example.com", password="password")
        response = self.client.post(reverse("my_account"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"].email, "example.example.example@example.com")
