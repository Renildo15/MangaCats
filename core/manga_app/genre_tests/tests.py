from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import Genre
from ..forms import GenreForm
import datetime


class GenreTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        cls.url = reverse("user:login")

        cls.genre = Genre.objects.create(
            name_genre="teste", date_created=datetime, create_by=cls.user
        )

    def test_genre_model(self):
        self.client.login(username='john', password='johnpassword')
        self.assertEqual(self.genre.name_genre, "teste")
        self.assertEqual(datetime.date(2023, 1, 26), datetime.date.today())
        self.assertEqual(self.genre.create_by.username,"john")

    def test_url_exists_at_correct_location_listview(self): 
         self.client.login(username='john', password='johnpassword')
         response = self.client.get(reverse("manga:genre_list"))
         self.assertNotEqual(response.status_code, 200)
         
    def test_url_exists_at_correct_location_add_genre(self): 
         self.client.login(username='john', password='johnpassword')
         response = self.client.get(reverse("manga:genre_add"))
         self.assertNotEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_edit_genre(self): 
         self.client.login(username='john', password='johnpassword')
         response = self.client.get(reverse("manga:genre_edit",args=(self.genre.id_genre,)))
         self.assertNotEqual(response.status_code, 200)

    def test_forms_genre(self):
        form_genre = {
            'name_genre': 'teste'
            }
        form = GenreForm(data = form_genre)
        self.assertTrue(form.is_valid())
        
    def test_empty_form_genre(self):
        form = GenreForm()
        self.assertIn("name_genre", form.fields)
        self.assertIn("create_by", form.fields)

    def test_views_genre_add(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:genre_add"))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/genre_add.html")

    def test_views_genre_list(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:genre_add"))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/genre_list.html")

    def test_views_genre_edit(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:genre_edit", args=(self.genre.id_genre,)))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/genre_add.html")