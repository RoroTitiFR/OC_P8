from django.test import TestCase

from app.models import PurBeurreUser


class TestAuthModels(TestCase):
    def test_user_model(self):
        """Test creating user works correctly
        """
        user = PurBeurreUser.objects.create_user("user@example.com", "password")
        self.assertEqual(str(user), "user@example.com")

    def test_create_user_with_no_email(self):
        """Test creating user with no email raises an error
        """
        self.assertRaises(ValueError, lambda: PurBeurreUser.objects.create_user(None, "password"))

    def test_superuser_model(self):
        """Test creating superuser works correctly
        """
        superuser = PurBeurreUser.objects.create_superuser("superuser@example.com", "password")
        self.assertEqual(str(superuser), "superuser@example.com")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.has_perm(None))
        self.assertTrue(superuser.has_module_perms(None))

    def test_create_superuser_with_fake_email(self):
        """Test creating user with no email raises an error
        """
        self.assertRaises(ValueError, lambda: PurBeurreUser.objects.create_superuser(None, "password"))
