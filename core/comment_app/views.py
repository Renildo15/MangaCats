from django.shortcuts import render, redirect, HttpResponseRedirect
from comment_app.forms import CommentChapterForm, CommentMangaForm
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.contrib import messages
from .models import CommentManga
# Create your views here.

def comment_list(pk):
    comment = CommentManga.objects.filter(manga=pk)
    return comment

