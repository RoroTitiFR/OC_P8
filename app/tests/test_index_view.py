from django.test import TestCase
from django.urls import reverse


class TestIndexView(TestCase):
    def test_index_view_url_exists_at_desired_location(self):
        """Test the index view URL exists
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_view_url_accessible_by_name(self):
        """Test the index view URL is accessible by name
        """
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        """Test the index view uses the correct template
        """
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/index.html")
        self.assertTemplateUsed(response, "app/layout.html")
        self.assertTemplateUsed(response, "app/navbar.html")

    def test_index_view_posting_form(self):
        """Test the search product form with POST request
        """
        data = {
            "search_term": "product"
        }
        response = self.client.post(reverse("index"), data)
        self.assertRedirects(response, reverse("results", kwargs={"search_term": "product"}))
