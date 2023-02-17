from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
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

        permission_view = Permission.objects.get(codename='view_genre')
        permission_add = Permission.objects.get(codename='add_genre')
        permission_change = Permission.objects.get(codename='change_genre')
        permission_delete = Permission.objects.get(codename='delete_genre')
        cls.user.user_permissions.add(permission_view)
        cls.user.user_permissions.add(permission_delete)
        cls.user.user_permissions.add(permission_add)
        cls.user.user_permissions.add(permission_change)

    def test_genre_model(self):
        self.client.login(username='john', password='johnpassword')
        self.assertEqual(self.genre.name_genre, "teste")
        self.assertEqual(datetime.date(2023, 2, 16), datetime.date.today())
        self.assertEqual(self.genre.create_by.username,"john")

    def test_url_exists_at_correct_location_genre_list(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:genre_list"))
        self.assertEqual(response.status_code, 200)
        
    def test_url_exists_at_correct_location_add_genre(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:genre_add"))
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_edit_genre(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:genre_edit",args=(self.genre.id_genre,)))
        self.assertEqual(response.status_code, 200)

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
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/genre/genre_add.html")

    def test_views_genre_list(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:genre_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/genre/genre_list.html")

    def test_views_genre_edit(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:genre_edit", args=(self.genre.id_genre,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/genre/genre_edit.html")