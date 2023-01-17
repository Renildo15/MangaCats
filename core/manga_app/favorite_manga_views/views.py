from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.http import JsonResponse
from ..models import FavoriteManga, Manga
from ..forms import FavoriteMangaForm
from django.contrib import messages

@login_required(login_url='user:login')
@permission_required("manga_app.view_favoritemanga", login_url='user:login')
def favorite_list(request):
    list_manga = FavoriteManga.objects.filter(user=request.user)

    context = {
        "mangas":list_manga
    }

    return render(request, "pages/favorite_manga/favorite_list.html", context)


@login_required(login_url='user:login')
@permission_required("manga_app.add_favoritemanga", login_url='user:login')
def favorite_manga(request):
    manga_id = request.GET.get('manga_id')
    manga = Manga.objects.get(id_manga=manga_id)
    print(manga_id)
    manga_favorite = FavoriteManga(favorite_manga=1,manga=manga,user=request.user)
    manga_favorite.save()
    data = {'status': 'favorite'}
    return JsonResponse(data)