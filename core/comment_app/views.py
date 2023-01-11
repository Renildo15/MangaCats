from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from comment_app.forms import CommentChapterForm, CommentMangaForm
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.contrib import messages
from .models import CommentManga, CommentChapter
from manga_app.models import Manga
from chapter_app.models import Chapter

# Create your views here.

def comment_list(pk):
    comment = CommentManga.objects.filter(manga=pk)
    return comment

def comment_edit(request, pk):
    comment = get_object_or_404(CommentManga, id_comment=pk)
    manga = Manga.objects.get(id_manga=comment.manga.id_manga)
    chapter = Chapter.objects.filter(manga_id=pk)
    manga_genre = manga.genre.all()
    form_comment = CommentMangaForm(instance=comment)
    comments = comment_list(comment.manga)

    if request.method == "POST":
        form_comment = CommentMangaForm(request.POST or None, instance=comment)

        if form_comment.is_valid():
            com = form_comment.save(commit=False)
            com.user = request.user
            com.manga = comment.manga.id_manga
            com.save()
            messages.success(request, "Comment successfully added!")
            return HttpResponseRedirect(reverse("manga:manga_view", args=(comment.manga.id_manga,))) 
        else:
            print("Invalid")

    context = {
        "form_comment":form_comment,
        "manga": manga,
        "manga_genre":manga_genre,
        'chapters':chapter,
        'form_comment':form_comment,
        "comments": comments,
    }
    return render(request, "pages/manga/manga_view.html", context)

def comment_delete(request, pk):
    comment = CommentManga.objects.get(id_comment=pk)
    id_manga = comment.manga.id_manga
    comment.delete()
    messages.success(request,"Comment deleted!")
    return redirect(reverse("manga:manga_view", args=(id_manga,)))