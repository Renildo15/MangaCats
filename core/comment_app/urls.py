from django.urls import path

app_name = "comment"
def test(request):
    pass
urlpatterns = [
    path("comment_list/", test, name="list")
]
