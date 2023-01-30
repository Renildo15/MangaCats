from ..models import HistoryManga
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse


def manga_history(manga, user):

    if not(HistoryManga.objects.filter(manga=manga, user=user).exists()):
        history = HistoryManga.objects.create(manga=manga, user=user)
        history.save()

        return history


def manga_history_list(request):
    history = HistoryManga.objects.filter(user=request.user).order_by('-view_date')

    context = {
        "manga_history":history
    }

    return render(request, "pages/history/manga_history.html", context)

def manga_history_reset(request):
    history = HistoryManga.objects.all()
    history.delete()
    messages.success(request, "History reseted!")
    return redirect(reverse("manga:manga_list"))
        

