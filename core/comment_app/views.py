from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from comment_app.forms import CommentChapterForm, CommentMangaForm
from django.http import JsonResponse
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

@login_required(login_url='user:login')
@permission_required({("comment.change_commentmanga","comment.add_commentmanga"), "comment.can_edit_comment", "comment.can_add_comment"}, login_url='user:login')
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
            com.manga = manga
            com.save()
            messages.success(request, "Comment successfully Edited!")
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

@login_required(login_url='user:login')
@permission_required({("comment.delete_commentmanga"), "comment.can_delete_comment"}, login_url='user:login')
def comment_delete(request):
    comment_id = request.GET.get('comment_id')
    comment = CommentManga.objects.get(id_comment=comment_id)
    comment.delete()
    messages.success(request,"Comment deleted!")
    data = {'status': 'delete'}
    return JsonResponse(data)


