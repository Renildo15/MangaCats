from ..models import HistoryManga
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from home_app.views import pagination_page

def manga_history(manga, user):

    if user.is_authenticated:
        if not(HistoryManga.objects.filter(manga=manga, user=user).exists()):
            history = HistoryManga.objects.create(manga=manga, user=user)
            history.save()

            return history

@login_required(login_url='user:login')
def manga_history_list(request):
    history = HistoryManga.objects.filter(user=request.user).order_by('-view_date')
    parameter_page = request.GET.get("page","1")
    parameter_limit = request.GET.get("limit","6")
    page = pagination_page(parameter_page, parameter_limit, history)

    context = {
        "manga_history":page,
        "qtn_pages": parameter_limit
    }

    return render(request, "pages/history/manga_history.html", context)


@login_required(login_url='user:login')
def manga_history_reset(request):
    history = HistoryManga.objects.all()
    history.delete()
    messages.success(request, "History reseted!")
    return redirect(reverse("manga:manga_list"))
        

