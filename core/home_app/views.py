from django.shortcuts import render
from manga_app.models import Manga
from chapter_app.models import Chapter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def manga_popular(request):
    laguage_pt = request.GET.get('PT-BR')
    laguage_jp = request.GET.get('JP')
    laguage_eng = request.GET.get('ENG')
    laguage_all = request.GET.get('ALL')
    search = request.GET.get("search")
    parameter_page = request.GET.get("page","1")
    parameter_limit = request.GET.get("limit", "6")
    language = ''

    manga_popular = Manga.objects.all().order_by('-views_manga')
    id_manga= manga_popular.values_list('id_manga', flat=True)
    _last = manga_id(id_manga)

    page = pagination_page(parameter_page, parameter_limit,manga_popular)

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
        "mangas":page,
        "last" : _last,
        "language":language,
        "qnt_page": parameter_limit
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


def pagination_page(page, limit, manga):
    if not (limit.isdigit() and int(limit) > 0):
        limit = "6"
    manga_paginator = Paginator(manga, limit)

    try:
        _page = manga_paginator.page(page)
    except(EmptyPage, PageNotAnInteger):
        _page = manga_paginator.page(1)

    return _page