from django.test import TestCase
from django.urls import reverse


class CourseBuilderViewTest(TestCase):
    def test_landing_page(self):
        url = reverse("coursebuilder:landing_page")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing_page.html")

    def test_about_page(self):
        url = reverse("coursebuilder:dynamic_about")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dynamic_about.html")

    def test_glossary_page(self):
        url = reverse("coursebuilder:dynamic_gloss")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dynamic_gloss.html")
