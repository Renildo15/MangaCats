from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from comment_app.forms import CommentChapterForm, CommentMangaForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.contrib import messages
from ..models import CommentManga, CommentChapter
from manga_app.models import Manga
from chapter_app.models import Chapter


def comment_chapter_list(pk):
    comment_chapter = CommentChapter.objects.filter(chapter=pk)
    return comment_chapter


@login_required(login_url='user:login')
@permission_required("comment_app.delete_commentchapter", login_url='user:login')
def comment_chapter_delete(request):
    comment_id = request.GET.get('comment_id')
    comment = CommentChapter.objects.get(id_comment=comment_id)
    comment.delete()
    messages.success(request,"Comment deleted!")
    data = {'status': 'delete'}
    return JsonResponse(data)

@login_required(login_url='user:login')
@permission_required("commentchapter.change_commentchapter", login_url='user:login')
def comment_chapter_edit(request, pk):
    comment_chapter = get_object_or_404(CommentChapter, id_comment=pk)
    chapter = Chapter.objects.get(id_chapter=comment_chapter.chapter.id_chapter)
    form_comment_chapter = CommentChapterForm(instance=comment_chapter)
    if request.user.is_authenticated:
        if request.method == "POST":
            form_comment_chapter = CommentChapterForm(request.POST or None, instance=comment_chapter)
            if form_comment_chapter.is_valid():
                com_ch = form_comment_chapter.save(commit=False)
                com_ch.user = request.user
                com_ch.chapter = chapter
                print(com_ch.chapter)
                com_ch.save()
                messages.success(request,"Comment successfully edited!")
                return redirect(reverse("chapter:page_list", args= (chapter.id_chapter,)))
    else:
        messages.warning(request, "You must be logged in to comment!")
    
    context = {
        'form_comment': form_comment_chapter
    }
    return render(request, "pages/comment/comment_edit.html", context)