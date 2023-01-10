from django.urls import path
from . import views
app_name = "comment"

urlpatterns = [
    path("comment_delete/<str:pk>", views.comment_delete, name="comment_delete"),
]
