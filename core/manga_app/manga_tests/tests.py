from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from ..models import Manga, Genre
from ..forms import MangaForm
import datetime


class MangaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        cls.genre = Genre.objects.create(
            name_genre="teste", date_created=datetime, create_by=cls.user
        )
        cls.url = reverse("user:login")
        
        cls.manga = Manga.objects.create(
            name_manga="teste", name_in_japanese="teste2", name_in_english="teste3",
            num_chapter=100, cover="foto.png", author="autor", status="on going", views_manga=1000,
            description="testetestetes", date_created=datetime, create_by=cls.user
        )
        permission_view = Permission.objects.get(codename='view_manga')
        permission_add = Permission.objects.get(codename='add_manga')
        permission_change = Permission.objects.get(codename='change_manga')
        permission_delete = Permission.objects.get(codename='delete_manga')
        cls.user.user_permissions.add(permission_view)
        cls.user.user_permissions.add(permission_delete)
        cls.user.user_permissions.add(permission_add)
        cls.user.user_permissions.add(permission_change)

    def test_manga_model(self):
        self.client.login(username='john', password='johnpassword')
        self.assertEqual(self.manga.name_manga, "teste")
        self.assertEqual(self.manga.name_in_japanese, "teste2")
        self.assertEqual(self.manga.name_in_english, "teste3")
        self.assertEqual(self.manga.num_chapter, 100)
        self.assertEqual(self.manga.cover, "foto.png")
        self.assertEqual(self.manga.author, "autor")
        self.assertEqual(self.manga.status, "on going")
        self.assertEqual(self.manga.views_manga, 1000)
        self.assertEqual(self.manga.description, "testetestetes")
        self.assertEqual(datetime.date(2023, 2, 16), datetime.date.today())
        self.assertEqual(self.manga.create_by.username,"john")
        
    def test_url_exists_at_correct_location_view_manga(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_list"))
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_add_manga(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_add"))
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_edit_manga(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_edit", args=(self.manga.id_manga,)))
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_list_manga(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_list"))
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_manga_uploaded(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_uploaded"))
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_corret_location_manga_delete(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(reverse("manga:manga_delete", args=(self.manga.id_manga,)))
        self.assertEqual(response.status_code, 302)

    # def test_forms_manga(self):
    #     form_manga = {
    #         'name_manga':'teste',
    #         'name_in_japanese':'teste2', 
    #         'name_in_english':'teste3',
    #         'num_chapter': 100, 
    #         'cover':'foto.png',
    #         'author':'autor', 
    #         'status':'on going', 
    #         'views_manga':1000,
    #         'description':'testetestetes'
    #     }

    #     form = MangaForm(data=form_manga)
    #     self.assertTrue(form.is_valid())


    def test_views_manga_add(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_add"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/manga_add.html")

    def test_views_manga_list(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/manga/manga_list.html")

    def test_views_manga_edit(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_edit", args=(self.manga.id_manga,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/manga/manga_edit.html")

    def test_views_manga_uploaded(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_uploaded"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/manga/manga_uploaded.html")

    def test_views_manga_view(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_view", args=(self.manga.id_manga,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/manga/manga_view.html")