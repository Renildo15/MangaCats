from django.shortcuts import render
from manga_app.models import Manga
from chapter_app.models import Chapter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def manga_popular(request):
    laguage_pt = request.GET.getlist('PT-BR')
    laguage_jp = request.GET.getlist('JP')
    laguage_eng = request.GET.getlist('ENG')
    laguage_all = request.GET.getlist('ALL')
    search = request.GET.get("search")
    parameter_page = request.GET.get("page","1")
    parameter_limit = request.GET.get("limit", "12")
    language = ''

    manga_popular = Manga.objects.all().order_by('-views_manga')
    id_manga= manga_popular.values_list('id_manga', flat=True)
    _last = manga_id(id_manga)

    if laguage_eng:
        manga_popular = Manga.objects.filter(language="ENG").order_by('-views_manga')
        id_manga= manga_popular.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)
        language = 'ENG'
        request.session['language'] = language

    elif laguage_pt: 
        manga_popular = Manga.objects.filter(language="PT-BR").order_by('-views_manga')
        id_manga= manga_popular.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)
        language = 'PT-BR'
        request.session['language'] = language
    
    elif laguage_jp:
        manga_popular = Manga.objects.filter(language="JP").order_by('-views_manga')
        id_manga= manga_popular.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)
        language = 'JP'
        request.session['language'] = language

    elif laguage_all:
        manga_popular = Manga.objects.all().order_by('-views_manga')
        id_manga= manga_popular.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)

    if search:
        manga_popular = manga_search(request, search)


    if "language" in request.session:
        language = request.session['language']

    page = pagination_page(parameter_page, parameter_limit,manga_popular)

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