from django.test import TestCase, Client
from django.contrib.auth.models import User
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
        self.assertEqual(datetime.date(2023, 1, 26), datetime.date.today())
        self.assertEqual(self.manga.create_by.username,"john")
        
    def test_url_exists_at_correct_location_view_manga(self): 
         self.client.login(username='john', password='johnpassword')
         response = self.client.get(reverse("manga:manga_list"))
         self.assertEqual(response.status_code, 200)
         
    def test_url_exists_at_correct_location_add_manga(self): 
         self.client.login(username='john', password='johnpassword')
         response = self.client.get(reverse("manga:manga_add"))
         self.assertNotEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_edit_manga(self): 
         self.client.login(username='john', password='johnpassword')
         response = self.client.get(reverse("manga:manga_edit",args=(self.genre.id_genre,)))
         self.assertNotEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_list_manga(self): 
         self.client.login(username='john', password='johnpassword')
         response = self.client.get(reverse("manga:manga_list"))
         self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_manga_uploaded(self): 
         self.client.login(username='john', password='johnpassword')
         response = self.client.get(reverse("manga:manga_uploaded"))
         self.assertNotEqual(response.status_code, 200)


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
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/manga_add.html")

    def test_views_manga_list(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/manga/manga_list.html")

    def test_views_manga_edit(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_edit", args=(self.manga.id_manga,)))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/manga/manga_edit.html")

    def test_views_manga_uploaded(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_uploaded"))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/manga/manga_uploaded.html")

    def test_views_manga_view(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_view", args=(self.manga.id_manga,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/manga/manga_view.html")