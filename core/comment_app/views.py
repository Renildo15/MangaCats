from django.shortcuts import render, redirect
from comment_app.forms import CommentChapterForm, CommentMangaForm
from django.urls import reverse
from django.contrib import messages
from .models import CommentManga
# Create your views here.
def comment_add(request, pk, manga):
    if request.method == "POST":
        form_comment = CommentMangaForm(request.POST or None)
        if form_comment.is_valid():
            comment = form_comment.save(commit = False)
            comment.user = request.user
            comment.manga = manga
            comment.save()
            messages.success(request, "Comment successfully added!")
            return redirect(reverse("manga:manga_view", args=(pk,)))
        else:
            print("Invalid")
    else:
          form_comment = CommentMangaForm()

    return form_comment

def comment_list(pk):
    comment = CommentManga.objects.filter(manga=pk)
    return comment

