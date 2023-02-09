from django.shortcuts import render
from manga_app.models import Manga
from chapter_app.models import Chapter
# Create your views here.

def manga_popular(request):
    laguage_pt = request.GET.get('PT-BR')
    laguage_jp = request.GET.get('JP')
    laguage_eng = request.GET.get('ENG')
    laguage_all = request.GET.get('ALL')
    search = request.GET.get("search")
    language = ''

    manga_popular = Manga.objects.all().order_by('-views_manga')
    id_manga= manga_popular.values_list('id_manga', flat=True)
    _last = manga_id(id_manga)

    if search:
        manga_popular = manga_search(request, search)
    
    if laguage_eng:
        manga_popular = Manga.objects.filter(language=laguage_eng).order_by('-views_manga')
        id_manga= manga_popular.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)
        language = 'ENG'
    elif laguage_pt: 
        manga_popular = Manga.objects.filter(language=laguage_pt).order_by('-views_manga')
        id_manga= manga_popular.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)
        language = 'PT-BR'
    elif laguage_jp:
        manga_popular = Manga.objects.filter(language=laguage_jp).order_by('-views_manga')
        id_manga= manga_popular.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)
        language = 'JP'
    elif laguage_all:
        manga_popular = Manga.objects.all().order_by('-views_manga')
        id_manga= manga_popular.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)

    context = {
        "mangas":manga_popular,
        "last" : _last,
        "language":language
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
    return _last
    
def manga_search(request, search):
    if search:
        if search != "" and search is not None:
            manga = Manga.objects.filter(name_manga__startswith = search)
            
            return manga