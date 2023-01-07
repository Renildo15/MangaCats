from django.urls import path
from chapter_app import views
from chapter_app.page_views import page_views

app_name="chapter"

urlpatterns = [
    path("pages/<str:pk>", page_views.page_list, name="page_list"),
    path("pages_add/<str:pk>", page_views.page_add, name="page_add"),
    path("chapter_list/<str:pk>", views.chapter_list, name="chapter_list"),
    path("chapter_add/<str:pk>", views.chapter_add, name="chapter_Add"),
    path("chapter_edit/<str:pk>", views.chapter_edit, name="chapter_edit"),
    path("chapter_delete/<str:pk>", views.chapter_delete, name="chapter_delete")
]
