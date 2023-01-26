from django.test import TestCase, Client
from ..models import Chapter
from ..forms import ChapterForm
from manga_app.models import Manga
from django.contrib.auth.models import User
from django.urls import reverse
import datetime


class ChapterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        cls.manga = Manga.objects.create(
            name_manga="teste", name_in_japanese="teste2", name_in_english="teste3",
            num_chapter=100, cover="foto.png", author="autor", status="on going", views_manga=1000,
            description="testetestetes", date_created=datetime, create_by=cls.user
        )

        cls.chapter = Chapter.objects.create(
            name_chapter="chapter - 01", manga = cls.manga, date_create = datetime, created_by = cls.user
        )

    def test_chapter_model(self):
        self.client.login(username='john', password='johnpassword')
        self.assertEqual(self.chapter.name_chapter, "chapter - 01")
        self.assertEqual(self.chapter.manga.name_manga, "teste")
        self.assertEqual(datetime.date(2023, 1, 26), datetime.date.today())
        self.assertEqual(self.chapter.created_by.username, 'john')

    def test_url_exists_at_correct_location_chapter_list_(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("chapter:chapter_list", args=(self.chapter.id_chapter,)))
        self.assertNotEqual(response.status_code, 200)
         
    def test_url_exists_at_correct_location_chapter_add(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("chapter:chapter_Add", args=(self.manga.id_manga,)))
        self.assertNotEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_chapter_edit(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_edit",args=(self.chapter.id_chapter,)))
        self.assertNotEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_chapter_delete(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("chapter:chapter_delete", args=(self.chapter.id_chapter,)))
        self.assertNotEqual(response.status_code, 200)



    def test_views_chapter_add(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("chapter:chapter_Add", args=(self.manga.id_manga,)))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/chapter/chapter_add.html")

    def test_views_chapter_list(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("chapter:chapter_list", args=(self.chapter.id_chapter,)))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/chapter/chapter_list.html")

    def test_views_chapter_edit(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("chapter:chapter_edit",args=(self.chapter.id_chapter,)))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/chapter/chapter_edit.html")


    def test_forms_chapter(self):
        form_chapter = {
            "name_chapter":"chapter - 01", 
            "manga": "qweqwefscscefef"
        }

        form = ChapterForm(data=form_chapter)
        self.assertFalse(form.is_valid())

    def test_empty_form_genre(self):
        form = ChapterForm()
        self.assertIn("name_chapter", form.fields)
        self.assertIn("manga", form.fields)