from django.test import TestCase
from django.urls import reverse


class HomepageTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/home.html")
        self.assertTemplateUsed(response, "app/layout.html")
        self.assertTemplateUsed(response, "app/navbar.html")
