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
    comment_chapter = CommentChapter.objects.filter(chapter=pk, active=False)
    return comment_chapter


def total_comments_chapter(pk):
    comment_chapter = CommentChapter.objects.filter(chapter=pk).count()
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
@permission_required("comment_app.change_commentchapter", login_url='user:login')
def comment_chapter_edit(request):
    data_id  = request.GET.get('data_id') 
    comment = request.GET.get('comment') 
    print(data_id, comment)

    comment_chapter = get_object_or_404(CommentChapter,id_comment=data_id) 
    comment_chapter.comment = comment 
    comment_chapter.save()   

    data = {'status':'update-item', 'comment':comment}
    return JsonResponse(data) 