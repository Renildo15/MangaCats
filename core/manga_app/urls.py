from django.urls import path
from manga_app import views
from manga_app.genre_views import views_genre

app_name="manga"

urlpatterns = [
   path("manga_list/", views.manga_list, name="manga_list"),
   path("manga_uploaded/", views.manga_uploaded, name="manga_uploaded"),
   path("manga_view/<str:pk>", views.manga_view, name="manga_view"),
   path("manga_edit/<str:pk>", views.manga_edit, name="manga_edit"),
   path("manga_add/", views.manga_add, name="manga_add"),
   path("genre_add/", views_genre.genre_add, name="genre_add"),
   path("genre_list/", views_genre.genre_list, name="genre_list"),
]
