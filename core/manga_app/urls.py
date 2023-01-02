from django.urls import path
from manga_app import views

app_name="manga"

urlpatterns = [
   path("manga_list/", views.manga_list, name="manga_list"),
   path("manga_add/", views.manga_add, name="manga_add"),
   path("genre_add/", views.genre_add, name="genre_add")
]
