from django.urls import path
from home_app import views

app_name = "home"

urlpatterns = [
    path("", views.manga_popular, name="home"),
]
