from django.urls import path
from chapter_app import views

app_name="chapter"

urlpatterns = [
    path("pages/<str:pk>", views.page_list, name="page_list")
]
