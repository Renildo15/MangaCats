from django.urls import path
from chapter_app import views

app_name="chapter"

urlpatterns = [
    path("pages/<str:pk>", views.page_list, name="page_list"),
    path("chapter_list/<str:pk>", views.chapter_list, name="chapter_list"),
    path("chapter_add/<str:pk>", views.chapter_add, name="chapter_Add"),
    path("chapter_edit/<str:pk>", views.chapter_edit, name="chapter_edit"),
    path("chapter_delete/<str:pk>", views.chapter_delete, name="chapter_delete")
]
