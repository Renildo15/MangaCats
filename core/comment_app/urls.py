from django.urls import path
from . import views
app_name = "comment"

urlpatterns = [
    path("comment_delete/", views.comment_delete, name="comment_delete"),
    path("comment_edit/<str:pk>", views.comment_edit, name="comment_edit")
]
