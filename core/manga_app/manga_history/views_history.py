from ..models import HistoryManga
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required


def manga_history(manga, user):

    if user.is_authenticated:
        if not(HistoryManga.objects.filter(manga=manga, user=user).exists()):
            history = HistoryManga.objects.create(manga=manga, user=user)
            history.save()

            return history

@login_required(login_url='user:login')
@permission_required("manga_app.view_historymanga", login_url='user:login')
def manga_history_list(request):
    history = HistoryManga.objects.filter(user=request.user).order_by('-view_date')

    context = {
        "manga_history":history
    }

    return render(request, "pages/history/manga_history.html", context)


@login_required(login_url='user:login')
@permission_required("manga_app.delete_historymanga", login_url='user:login')
def manga_history_reset(request):
    history = HistoryManga.objects.all()
    history.delete()
    messages.success(request, "History reseted!")
    return redirect(reverse("manga:manga_list"))
        
