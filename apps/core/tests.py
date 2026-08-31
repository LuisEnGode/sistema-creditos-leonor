from django.test import TestCase
from django.urls import reverse


class HealthApiTests(TestCase):
    def test_health_endpoint(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


class CoreViewTests(TestCase):
    def test_home_loads(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")

    def test_htmx_test_returns_partial(self):
        response = self.client.get(reverse("htmx_test"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "core/partials/htmx_response.html",
        )
        self.assertContains(
            response,
            "HTMX está funcionando correctamente",
        )
