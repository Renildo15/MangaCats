from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import CommentManga
from .models import CommentManga
from home_app.views import pagination_page

# Create your views here.

def comment_list(request,pk):
    parameter_page = request.GET.get("page","1")
    parameter_limit = request.GET.get("limit","12")
    comment = CommentManga.objects.filter(manga=pk, active=False)
    page = pagination_page(parameter_page,parameter_limit, comment)
    context = {
        "comment":page,
        "qnt_page": parameter_limit
    }
    return context

def total_comments_manga(pk):
    total_comments = CommentManga.objects.filter(manga=pk).count()
    return total_comments

@login_required(login_url='user:login')
def comment_edit(request):
    data_id  = request.GET.get('data_id') 
    comment = request.GET.get('comment') 
    print(data_id, comment)

    comment_manga = get_object_or_404(CommentManga,id_comment=data_id) 
    comment_manga.comment = comment 
    comment_manga.save()   

    data = {'status':'update-item', 'comment':comment}
    return JsonResponse(data) 

@login_required(login_url='user:login')
def comment_delete(request):
    comment_id = request.GET.get('comment_id')
    comment = CommentManga.objects.get(id_comment=comment_id)
    comment.delete()
    messages.success(request,"Comment deleted!")
    data = {'status': 'delete'}
    return JsonResponse(data)
