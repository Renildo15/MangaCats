from django.shortcuts import get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from ..models import StatusManga, Manga


#TODO: Adicionar a remoção do status do banco de dados quando clicar em not_read
def status_manga(request):
    manga_status_val = request.GET.get('status_val')
    manga_id = request.GET.get('manga_id')
    
    status = ''
   
    if StatusManga.objects.filter(manga=manga_id, user=request.user).exists():
        if manga_status_val == "not_read":
            st = get_object_or_404(StatusManga, manga=manga_id, user=request.user)
            st.delete()
            status="deleted"
        _status = get_object_or_404(StatusManga, manga=manga_id, user = request.user)
        _status.status = manga_status_val
        _status.save()
        status="changed"
    else:
        manga = get_object_or_404(Manga, id_manga=manga_id)
        user = request.user
        manga_status = StatusManga(status=manga_status_val, manga=manga, user=user)
        manga_status.save()
        status="Added"
    data = {
        "status":status,
        "manga_status_val":manga_status_val
    }
    return JsonResponse(data)


def status_selected(request,pk):
    manga = get_object_or_404(Manga, id_manga=pk)
    status_manga = get_object_or_404(StatusManga, manga=manga, user=request.user)
    return status_manga
