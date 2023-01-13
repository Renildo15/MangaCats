from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from comment_app.forms import CommentChapterForm, CommentMangaForm
from django.urls import reverse
from .models import Manga
from chapter_app.models import Chapter
from .forms import MangaForm
from django.contrib import messages
from comment_app.views import comment_list, comment_edit

# Create your views here.

def manga_list(request):
    manga = Manga.objects.all()
    
    context = {
        "mangas": manga,
    }
    return render(request,"pages/manga/manga_list.html", context)

@login_required(login_url='user:login')
@permission_required({("manga.view_manga"), "manga.can_view_manga"}, login_url='user:login')
def manga_uploaded(request):
    manga = Manga.objects.filter(create_by=request.user)
    context = {
        "mangas": manga
    }
    return render(request,"pages/manga/manga_uploaded.html", context)


def manga_view(request, pk):
    manga = Manga.objects.get(id_manga=pk)
    chapter = Chapter.objects.filter(manga_id=pk)
    manga_genre = manga.genre.all()
    form_comment = CommentMangaForm()
    comment = comment_list(pk)
   
    if request.method == "POST":
        if request.user.is_authenticated:
            form_comment = CommentMangaForm(request.POST or None)
            if form_comment.is_valid():
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
    }

    return render(request, "pages/manga/manga_view.html", context)

@login_required(login_url='user:login')
@permission_required({("manga.add_manga"), "manga.can_add_manga"}, login_url='user:login')
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
@permission_required({("manga.change_manga"), "manga.can_edit_manga"}, login_url='user:login')
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
@permission_required({("manga.delete_manga"), "manga.can_delete_manga"}, login_url='user:login')
def manga_delete(request, pk):
    manga = get_object_or_404(Manga, id_manga=pk)
    manga.delete()
    messages.warning(request, f"Manga {manga.name_manga} deleted!")
    return redirect('manga:manga_uploaded')