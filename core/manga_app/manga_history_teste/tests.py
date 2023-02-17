from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
from manga_app.models import Manga, HistoryManga
import datetime
from django.urls import reverse

class HistoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        cls.manga = Manga.objects.create(
            name_manga="teste", name_in_japanese="teste2", name_in_english="teste3",
            num_chapter=100, cover="foto.png", author="autor", status="on going", views_manga=1000,
            description="testetestetes", date_created=datetime, create_by=cls.user
        ) 

        cls.manga_history = HistoryManga.objects.create(
            manga = cls.manga, user =cls.user, view_date = datetime
        )
        # Adiciona permissão de acesso à view de histórico de mangás para o usuário 'john'
        permission_view = Permission.objects.get(codename='view_historymanga')
        permission_delete = Permission.objects.get(codename='delete_historymanga')
        cls.user.user_permissions.add(permission_view)
        cls.user.user_permissions.add(permission_delete)


    def test_history_models(self):
        self.client.login(username='john', password='johnpassword')
        self.assertEqual(self.manga.name_manga, "teste")
        self.assertEqual(self.user.username, "john")
        self.assertEqual(datetime.date(2023, 2, 16), datetime.date.today())

    def test_url_exists_history_list(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_history"))
        self.assertEqual(response.status_code, 200)

    def test_url_exists_history_reset(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(reverse('manga:manga_history_reset'))
        self.assertEqual(response.status_code, 302)


    def test_manga_history_list_view(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("manga:manga_history"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/history/manga_history.html")

    def test_manga_history_view(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(reverse("manga:manga_history"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(HistoryManga.objects.filter(manga=self.manga, user=self.user).exists()) # Verifica se o registro foi criado