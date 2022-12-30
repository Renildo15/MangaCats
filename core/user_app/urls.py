from django.urls import path
from user_app import views


app_name = "user"

urlpatterns = [
    path("register/", views.register_user, name="register")
]
