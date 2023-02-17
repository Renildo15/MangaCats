from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from comment_app.forms import CommentMangaForm
from comment_app.models import CommentManga
from django.urls import reverse
from .models import Manga
from chapter_app.models import Chapter
from .forms import MangaForm
from django.contrib import messages
from comment_app.views import comment_list, total_comments_manga
from .favorite_manga_views.views import favorite_button
from .manga_review_views.views import review_avarege, review_selected
from .status_manga_views.views import status_selected
from .manga_history.views_history import manga_history
from home_app.views import  manga_id, manga_search, pagination_page

# Create your views here.

def manga_list(request):
    laguage_pt = request.GET.getlist('PT-BR')
    laguage_jp = request.GET.getlist('JP')
    laguage_eng = request.GET.getlist('ENG')
    laguage_all = request.GET.getlist('ALL')
    search = request.GET.get("search")
    parameter_page = request.GET.get("page","1")
    parameter_limit = request.GET.get("limit", "12")
    language = ''

    manga = Manga.objects.all().order_by('name_manga')
    id_manga= manga.values_list('id_manga', flat=True)
    _last = manga_id(id_manga)

    page = pagination_page(parameter_page, parameter_limit, manga)

    if laguage_eng:
        manga = Manga.objects.filter(language='ENG').order_by('name_manga')
        id_manga= manga.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)
        language = 'ENG'
        request.session['language'] = language

    elif laguage_pt: 
        manga = Manga.objects.filter(language='PT-BR').order_by('name_manga')
        id_manga= manga.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)
        language = 'PT-BR'
        request.session['language'] = language

    elif laguage_jp:
        manga = Manga.objects.filter(language='JP').order_by('name_manga')
        id_manga= manga.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)
        language = 'JP'
        request.session['language'] = language

    elif laguage_all:
        manga = Manga.objects.all().order_by('name_manga')
        id_manga= manga.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)

    if search:
        manga = manga_search(request, search)

    if "language" in request.session:
        language = request.session['language']
    page = pagination_page(parameter_page, parameter_limit, manga)
    context = {
        "mangas":page,
        "last":_last,
        "qnt_page": parameter_limit,
        "language":language
    }
    return render(request,"pages/manga/manga_list.html", context)



@login_required(login_url='user:login')
@permission_required("manga_app.view_manga", login_url='user:login')
def manga_uploaded(request):
    parameter_page = request.GET.get("page","1")
    parameter_limit = request.GET.get("limit","6")
    manga = Manga.objects.filter(create_by=request.user)
    id_manga= manga.values_list('id_manga', flat=True)
    _last = manga_id(id_manga)

    page = pagination_page(parameter_page, parameter_limit, manga)
    context = {
        "mangas": page,
        "last":_last
    }
    return render(request,"pages/manga/manga_uploaded.html", context)


def manga_view(request, pk):
    manga = Manga.objects.get(id_manga=pk)
    if manga.update_type != 'content':
        manga.views_manga += 1
        manga.update_type = 'views'
    manga.save()


    chapter = Chapter.objects.filter(manga_id=pk)
    manga_genre = manga.genre.all()
    form_comment = CommentMangaForm()

    user = request.user
    history = manga_history(manga, user)
    total_comments = total_comments_manga(pk)
    comment = comment_list(request,pk)
    re_ave = review_avarege(pk)
    reviews = re_ave['total_reviews']
    average = re_ave['average']

    try:
        status = status_selected(request,pk)
    except:   
        status = None
    try:
        favorites = favorite_button(request,pk)
    except:
        favorites = None

    try:
        re_sel = review_selected(request,pk)
    except:
        re_sel = None

    if request.method == "POST":
        if request.user.is_authenticated:
            form_comment = CommentMangaForm(request.POST or None)
            if form_comment.is_valid():
                parent_obj = None
                try:
                    parent_id = request.POST.get('parent_id')
                except:
                    parent_id = None

                if parent_id:
                    parent_obj = CommentManga.objects.get(id_comment=parent_id)
                    if parent_obj:
                        replay_comment = form_comment.save(commit=False)
                        replay_comment.parent = parent_obj
                        replay_comment.active = True
                comment = form_comment.save(commit = False)
                comment.user = request.user
                comment.manga = manga
                comment.save()
                messages.success(request, "Comment successfully added!")
                return HttpResponseRedirect(reverse("manga:manga_view", args=(pk,))) 
            else:
                print("Invalid")
        else:
            messages.warning(request, "You must be logged in to comment!")
    else:
        form_comment = CommentMangaForm()

        
    context = {
        "manga": manga,
        "manga_genre":manga_genre,
        'chapters':chapter,
        'form_comment':form_comment,
        "comments": comment["comment"],
        "qnt_page":comment["qnt_page"],
        'total_comments': total_comments,
        'favorites': favorites,
        "average":average,
        'reviews':reviews,
        're_sel': re_sel,
        "status":status,
        "manga_id":pk
    }

    return render(request, "pages/manga/manga_view.html", context)

@login_required(login_url='user:login')
@permission_required("manga_app.add_manga", login_url='user:login')
def manga_add(request):
    if request.method == 'POST':
        form_manga = MangaForm(request.POST or None, request.FILES,request=request)
        if form_manga.is_valid():
            manga = form_manga.save(commit=False)
            manga.create_by = request.user
            manga.save()
            form_manga.save_m2m()
            messages.success(request,"Manga added!")

            return redirect(reverse("home:home"))
        else:
            print("Problema")
    else:
        form_manga = MangaForm(request=request)

    context = {
        "form_manga" : form_manga
    }

    return render(request, "pages/manga/manga_add.html", context)


@login_required(login_url='user:login')
@permission_required("manga_app.change_manga", login_url='user:login')
def manga_edit(request, pk):
    manga = get_object_or_404(Manga, id_manga=pk)
    form_manga = MangaForm(instance=manga, request=request)
    if request.method == "POST":
        form_manga = MangaForm(request.POST or None, request.FILES, instance=manga, request=request)
        if form_manga.is_valid():
            manga = form_manga.save(commit=False)
            manga.create_by = request.user
            manga.save()
            form_manga.save_m2m()
            messages.success(request, f"Manga {manga.name_manga} updated!")
            return redirect('manga:manga_uploaded')
    elif(request.method == 'GET'):
        return render(request, "pages/manga/manga_edit.html", {'form_manga': form_manga})

    return render(request, "pages/manga/manga_edit.html", {'form_manga': form_manga})


@login_required(login_url='user:login')
@permission_required({("manga_app.delete_manga"), "manga.can_delete_manga"}, login_url='user:login')
def manga_delete(request, pk):
    manga = get_object_or_404(Manga, id_manga=pk)
    manga.delete()
    messages.warning(request, f"Manga {manga.name_manga} deleted!")
    return redirect('manga:manga_uploaded')



            
