from django.test import TestCase
from django.urls import reverse
# Create your tests here.

class HomePageTest(TestCase):

    def test_url_exists_at_correct_location(self):
        response = self.client.get(reverse("home:home"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,"pages/home.html")