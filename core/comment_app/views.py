from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404, HttpResponse
from comment_app.forms import CommentChapterForm, CommentMangaForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.contrib import messages
from .models import CommentManga, CommentChapter
from .models import CommentManga
from manga_app.models import Manga
from chapter_app.models import Chapter

# Create your views here.

def comment_list(pk):
    comment = CommentManga.objects.filter(manga=pk, active=False)
    return comment

@login_required(login_url='user:login')
@permission_required("comment_app.can_edit_comment", login_url='user:login')
def comment_edit(request):
    data_id  = request.GET.get('data_id') # Id da Lista
    comment = request.GET.get('comment') # Id do status
    print(data_id, comment)

    comment_manga = get_object_or_404(CommentManga,id_comment=data_id) # Get Objeto lista
    comment_manga.comment = comment # status recebe novo valor "Id do status"
    comment_manga.save() # salva  

    data = {'status':'update-item', 'comment':comment}
    return JsonResponse(data) # retorna

@login_required(login_url='user:login')
@permission_required("comment_app.delete_commentmanga", login_url='user:login')
def comment_delete(request):
    comment_id = request.GET.get('comment_id')
    comment = CommentManga.objects.get(id_comment=comment_id)
    comment.delete()
    messages.success(request,"Comment deleted!")
    data = {'status': 'delete'}
    return JsonResponse(data)
