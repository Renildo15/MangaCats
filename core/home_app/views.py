from django.shortcuts import render
from manga_app.models import Manga
from chapter_app.models import Chapter
# Create your views here.

def manga_popular(request):
    manga_popular = Manga.objects.all().order_by('-views_manga')
    id_manga= manga_popular.values_list('id_manga', flat=True)
    _last = manga_id(id_manga)
      
    context = {
        "mangas":manga_popular,
        "last" : _last
    }

    return render(request,"pages/home.html", context)

def last(pk):
    chapter = Chapter.objects.filter(manga=pk)
    return chapter.last()

def manga_id(manga_id):
    _last = []
    for pk in manga_id:
        _last_page = last(pk)
        if _last_page != None:
           _last.append(_last_page)
        else:
            print("Caiu aqui")

    return _last
    