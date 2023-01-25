from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from comment_app.forms import CommentChapterForm, CommentMangaForm
from comment_app.models import CommentManga
from django.urls import reverse
from .models import Manga
from chapter_app.models import Chapter
from .forms import MangaForm
from django.contrib import messages
from comment_app.views import comment_list, total_comments_manga
from .favorite_manga_views.views import favorite_button
from .manga_review_views.views import review_avarege, review_selected
from home_app.views import  manga_id

# Create your views here.

def manga_list(request):
    laguage_pt = request.GET.get('PT-BR')
    laguage_jp = request.GET.get('JP')
    laguage_eng = request.GET.get('ENG')
    laguage_all = request.GET.get('ALL')

    manga = Manga.objects.all().order_by('-views_manga')
    id_manga= manga.values_list('id_manga', flat=True)
    _last = manga_id(id_manga)
    
    if laguage_eng:
        manga = Manga.objects.filter(language=laguage_eng).order_by('-views_manga')
        id_manga= manga.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)
    elif laguage_pt: 
        manga = Manga.objects.filter(language=laguage_pt).order_by('-views_manga')
        id_manga= manga.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)
    elif laguage_jp:
        manga = Manga.objects.filter(language=laguage_jp).order_by('-views_manga')
        id_manga= manga.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)
    elif laguage_all:
        manga = Manga.objects.all().order_by('-views_manga')
        id_manga= manga.values_list('id_manga', flat=True)
        _last = manga_id(id_manga)
    
    context = {
        "mangas":manga,
        "last":_last
    }
    return render(request,"pages/manga/manga_list.html", context)



@login_required(login_url='user:login')
@permission_required("manga_app.view_manga", login_url='user:login')
def manga_uploaded(request):
    manga = Manga.objects.filter(create_by=request.user)
    id_manga= manga.values_list('id_manga', flat=True)
    _last = manga_id(id_manga)
    context = {
        "mangas": manga,
        "last":_last
    }
    return render(request,"pages/manga/manga_uploaded.html", context)




def manga_view(request, pk):
    manga = Manga.objects.get(id_manga=pk)
    chapter = Chapter.objects.filter(manga_id=pk)
    manga_genre = manga.genre.all()
    form_comment = CommentMangaForm()


    total_comments = total_comments_manga(pk)
    comment = comment_list(pk)
    re_ave = review_avarege(pk)
    reviews = re_ave['total_reviews']
    average = re_ave['average']
   

    try:
         re_sel = review_selected(request,pk)
    except:
          re_sel = None

    try:
        favorites = favorite_button(request,pk)
        re_sel = review_selected(request,pk)
    except:
        favorites = None
      
    
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
        "comments": comment,
        'total_comments': total_comments,
        'favorites': favorites,
        "average":average,
        'reviews':reviews,
        're_sel': re_sel
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