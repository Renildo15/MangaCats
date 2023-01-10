from django.shortcuts import render, redirect, HttpResponseRedirect
from comment_app.forms import CommentChapterForm, CommentMangaForm
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.contrib import messages
from .models import CommentManga, CommentChapter

# Create your views here.

def comment_list(pk):
    comment = CommentManga.objects.filter(manga=pk)
    return comment

def comment_delete(request, pk):
    comment = CommentManga.objects.get(id_comment=pk)
    id_manga = comment.manga.id_manga
    comment.delete()
    messages.success(request,"Comment deleted!")
    return redirect(reverse("manga:manga_view", args=(id_manga,)))