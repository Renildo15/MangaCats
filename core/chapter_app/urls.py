from django.urls import path
from chapter_app import views

app_name="chapter"

urlpatterns = [
    path("pages/<str:pk>", views.page_list, name="page_list"),
    path("chapter_list/<str:pk>", views.chapter_list, name="chapter_list")
]
