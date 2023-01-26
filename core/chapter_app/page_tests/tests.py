from django.test import TestCase, Client
from ..models import Chapter, Page
from manga_app.models import Manga
from ..forms import PageForm
from django.contrib.auth.models import User
from django.urls import reverse
import datetime



class PagesTests(TestCase):
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

        cls.page = Page.objects.create(
            image_chapter="http://www.teste/imagge.jpg", chapter_name = cls.chapter,  created_by = cls.user
        )

    def test_chapter_model(self):
        self.client.login(username='john', password='johnpassword')
        self.assertEqual(self.page.image_chapter, "http://www.teste/imagge.jpg")
        self.assertEqual(self.page.chapter_name.name_chapter, "chapter - 01")
        self.assertEqual(self.page.created_by.username, 'john')

    
    # def test_url_exists_at_correct_location_page_list(self): 
    #     self.client.login(username='john', password='johnpassword')
    #     response = self.client.get(reverse("chapter:page_list", args=(self.page.id_img,)))
    #     self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_page_list_manager(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("chapter:page_list_manager", args=(self.page.id_img,)))
        self.assertNotEqual(response.status_code, 200)
         
    def test_url_exists_at_correct_location_page_add(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("chapter:page_add", args=(self.chapter.id_chapter,)))
        self.assertNotEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_page_edit(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("chapter:page_edit",args=(self.page.id_img,)))
        self.assertNotEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_page_delete(self): 
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("chapter:page_delete", args=(self.page.id_img,)))
        self.assertNotEqual(response.status_code, 200)


    def test_views_page_add(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("chapter:page_add", args=(self.chapter.id_chapter,)))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/page/page_add.html")

    def test_views_page_list(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("chapter:page_list", args=(self.chapter.id_chapter,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/page/page_list.html")

    def test_views_page_list_manager(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("chapter:page_list_manager", args=(self.chapter.id_chapter,)))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/page/page_list_manager.html")

    def test_views_page_edit(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("chapter:page_edit",args=(self.page.id_img,)))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/chapter/chapter_edit.html")


    def test_forms_page(self):
        form_chapter = {
           "image_chapter":"http://www.teste/imagge.jpg", 
          " chapter_name" : "derewfawefecdsfwe"
        }

        form = PageForm(data=form_chapter)
        self.assertTrue(form.is_valid())

    def test_empty_form_genre(self):
        form = PageForm()
        self.assertIn("image_chapter", form.fields)
        self.assertIn("chapter_name", form.fields)