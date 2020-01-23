from django.test import TestCase

from app.forms.auth import CustomUserCreationForm, CustomUserChangeForm
from app.forms.search_product import SearchProductForm


class TestForms(TestCase):
    def test_search_product_form_with_valid_data(self):
        """Test the search product form is valid when correct data provided
        """
        register_form = SearchProductForm(data={
            "search_term": "product"
        })
        self.assertTrue(register_form.is_valid())

    def test_search_product_form_with_invalid_data(self):
        """Test the search product form is invalid with incorrect data provided
        """
        register_form = SearchProductForm(data={
            "search_term": None
        })
        self.assertFalse(register_form.is_valid())

    def test_register_form_with_valid_data(self):
        """Test the register form is valid when correct data provided
        """
        register_form = CustomUserCreationForm(data={
            "email": "example@example.com",
            "password1": "pexoyeH9B@!t-aChastU",
            "password2": "pexoyeH9B@!t-aChastU"
        })
        self.assertTrue(register_form.is_valid())

    def test_register_form_with_fake_email(self):
        """Test the register form is invalid when incorrect email provided
        """
        register_form = CustomUserCreationForm(data={
            "email": "example@example",
            "password1": "pexoyeH9B@!t-aChastU",
            "password2": "pexoyeH9B@!t-aChastU"
        })
        self.assertFalse(register_form.is_valid())
        for error in register_form.errors:
            self.assertIn("is-danger", register_form.fields[error].widget.attrs["class"])

    def test_register_form_with_short_password(self):
        """Test the register form is invalid when short password provided
        """
        register_form = CustomUserCreationForm(data={
            "email": "example@example.com",
            "password1": "H9B@!t",
            "password2": "H9B@!t"
        })
        self.assertFalse(register_form.is_valid())
        for error in register_form.errors:
            self.assertIn("is-danger", register_form.fields[error].widget.attrs["class"])

    def test_register_form_with_common_password(self):
        """Test the register form is invalid when common password provided
        """
        register_form = CustomUserCreationForm(data={
            "email": "example@example.com",
            "password1": "azerty123",
            "password2": "azerty123"
        })
        self.assertFalse(register_form.is_valid())
        for error in register_form.errors:
            self.assertIn("is-danger", register_form.fields[error].widget.attrs["class"])

    def test_change_user_form_with_valid_data(self):
        """Test the change user form is valid when correct data provided"""
        change_user_form = CustomUserChangeForm(data={
            "email": "example@example.com",
        })
        self.assertTrue(change_user_form.is_valid())
        for error in change_user_form.errors:
            self.assertIn("is-danger", change_user_form.fields[error].widget.attrs["class"])

    def test_change_user_form_with_fake_email(self):
        """Test the change user form is invalid when incorrect data provided"""
        change_user_form = CustomUserChangeForm(data={
            "email": "example@example",
        })
        self.assertFalse(change_user_form.is_valid())
        for error in change_user_form.errors:
            self.assertIn("is-danger", change_user_form.fields[error].widget.attrs["class"])
