from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.contrib import messages
from ..models import CommentChapter
from home_app.views import pagination_page



def comment_chapter_list(request,pk):
    parameter_page = request.GET.get("page","1")
    parameter_limit = request.GET.get("limit","12")
    comment_chapter = CommentChapter.objects.filter(chapter=pk, active=False)
    page = pagination_page(parameter_page,parameter_limit, comment_chapter)
    context = {
        "comment_chapter":page,
        "qnt_page": parameter_limit
    }
    return context


def total_comments_chapter(pk):
    comment_chapter = CommentChapter.objects.filter(chapter=pk).count()
    return comment_chapter


@login_required(login_url='user:login')
def comment_chapter_delete(request):
    comment_id = request.GET.get('comment_id')
    comment = CommentChapter.objects.get(id_comment=comment_id)
    comment.delete()
    messages.success(request,"Comment deleted!")
    data = {'status': 'delete'}
    return JsonResponse(data)

@login_required(login_url='user:login')
def comment_chapter_edit(request):
    data_id  = request.GET.get('data_id') 
    comment = request.GET.get('comment') 
    print(data_id, comment)

    comment_chapter = get_object_or_404(CommentChapter,id_comment=data_id) 
    comment_chapter.comment = comment 
    comment_chapter.save()   

    data = {'status':'update-item', 'comment':comment}
    return JsonResponse(data) 