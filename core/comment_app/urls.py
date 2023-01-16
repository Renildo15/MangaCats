from django.urls import path
from . import views
from .comment_chapter import views as chapter_views

app_name = "comment"

urlpatterns = [
    path("comment_delete/", views.comment_delete, name="comment_delete"),
    path("comment_edit/", views.comment_edit, name="comment_edit"),
    path("comment_chapter_delete/", chapter_views.comment_chapter_delete, name="comment_chapter_delete"),
    path("comment_chapter_edit/<str:pk>", chapter_views.comment_chapter_edit, name="comment_chapter_edit"),
]
