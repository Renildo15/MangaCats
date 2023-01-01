from django.shortcuts import render
from .models import Manga
# Create your views here.

def manga_list(request):
    manga = Manga.objects.all()
    context = {
        "mangas": manga
    }
    return render(request,"pages/manga_list.html", context)
