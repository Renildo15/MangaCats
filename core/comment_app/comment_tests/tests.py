from django.test import TestCase, Client
from django.contrib.auth.models import User
from ..models import CommentManga
from ..forms import CommentMangaForm
from manga_app.models import Manga
import datetime
from django.urls import reverse

class CommentsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        cls.manga = Manga.objects.create(
            name_manga="teste", name_in_japanese="teste2", name_in_english="teste3",
            num_chapter=100, cover="foto.png", author="autor", status="on going", views_manga=1000,
            description="testetestetes", date_created=datetime, create_by=cls.user
        )
        cls.reply = CommentManga.objects.create(
            comment="Teste", date_created=datetime, user=cls.user, manga=cls.manga, active=True
        )
        cls.comment = CommentManga.objects.create(
            comment="Teste", date_created=datetime, user=cls.user, manga=cls.manga, active=True, parent=cls.reply
        )

    def test_comment_model(self):
        self.client.login(username='john', password='johnpassword')
        self.assertEqual(self.comment.comment, "Teste")
        self.assertEqual(datetime.date(2023, 1, 26), datetime.date.today())
        self.assertEqual(self.comment.user.username, "john")
        self.assertEqual(self.comment.manga.name_manga, "teste")
        self.assertEqual(self.comment.active, True)

    def test_url_exists_at_correct_location_comment_edit(self): 
         self.client.login(username='john', password='johnpassword')
         response = self.client.get(reverse("comment:comment_edit"))
         self.assertNotEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_comment_delete(self): 
         self.client.login(username='john', password='johnpassword')
         response = self.client.get(reverse("comment:comment_delete"))
         self.assertNotEqual(response.status_code, 200)

    def test_forms_comment(self):
        form_comment = {
           'comment': 'Teste'
        }

        form = CommentMangaForm(data=form_comment)
        self.assertTrue(form.is_valid())


    def test_view_comment_edit(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("comment:comment_edit"))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/manga/manga_view.html")

    def test_view_comment_delete(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("comment:comment_delete"))
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "pages/manga/manga_view.html")


         
    
         
   
    

