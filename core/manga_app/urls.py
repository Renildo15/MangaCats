from django.urls import path
from manga_app import views
from manga_app.genre_views import views_genre
from manga_app.favorite_manga_views import views as favorite_views
from manga_app.status_manga_views import views as status_views
from manga_app.manga_review_views.views import manga_review
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name="manga"

urlpatterns = [
   path("manga_list/", views.manga_list, name="manga_list"),
   path("manga_uploaded/", views.manga_uploaded, name="manga_uploaded"),
   path("manga_view/<str:pk>/", views.manga_view, name="manga_view"),
   path("manga_edit/<str:pk>/", views.manga_edit, name="manga_edit"),
   path("manga_delete/<str:pk>/", views.manga_delete, name="manga_delete"),
   path("manga_add/", views.manga_add, name="manga_add"),
   path("genre/", views_genre.genre, name="genre"),
   path("genre/<str:name_genre>/<str:pk>", views_genre.genre_filter, name="genre_manga"),
   path("genre_add/", views_genre.genre_add, name="genre_add"),
   path("genre_list/", views_genre.genre_list, name="genre_list"),
   path("genre_edit/<str:pk>", views_genre.genre_edit, name="genre_edit"),
   path("genre_delete/<str:pk>", views_genre.genre_delete, name="genre_delete"),
   path("favorite_add/",favorite_views.favorite_manga, name="favorite_manga"),
   path("favorite_list/", favorite_views.favorite_list, name="favorite_list"),
   path("favorite_remove/", favorite_views.favorite_remove, name="favorite_remove"),
   path("manga_review/",manga_review, name="manga_review" ),
   path("manga_status/", status_views.status_manga, name="manga_status"),
   path("manga_list_by_status/<str:status>",status_views.status, name="list_status" ),
]
urlpatterns += staticfiles_urlpatterns()