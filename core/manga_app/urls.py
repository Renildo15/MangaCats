from django.urls import path
from manga_app import views
app_name="manga"

urlpatterns = [
   path("manga_list/", views.manga_list, name="manga_list")
]
