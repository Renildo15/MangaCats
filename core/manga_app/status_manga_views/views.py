from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from ..models import StatusManga, Manga

@login_required(login_url='user:login')
@permission_required("manga_app.add_statusmanga", login_url='user:login')
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

@login_required(login_url='user:login')
@permission_required("manga_app.view_statusmanga", login_url='user:login')
def status(request, status):
    manga_reading = StatusManga.objects.filter(status=status, user=request.user)
    title = status_title(status)
    total_list = manga_reading.count()
    context = {
        "manga_reading":manga_reading,
        "total_list":total_list,
        "title": title
    }
    return render(request,"pages/status/status.html", context)


def status_title(status):
    if status == "reading":
        title = "Reading"
        return title
    elif status == "dropped":
        title = "Dropped"
        return title
    elif status == "completed":
        title = "Completed"
        return title
    else:
        title = "Plan to Read"
        return title





