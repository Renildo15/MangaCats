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

def comment_chapter_delete(request):
    comment_id = request.GET.get('comment_id')
    comment = CommentChapter.objects.get(id_comment=comment_id)
    comment.delete()
    messages.success(request,"Comment deleted!")
    data = {'status': 'delete'}
    return JsonResponse(data)