from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Manga
from .forms import MangaForm, GenreForm
from django.contrib import messages
# Create your views here.

def manga_list(request):
    manga = Manga.objects.all()
    context = {
        "mangas": manga
    }
    return render(request,"pages/manga_list.html", context)


def manga_add(request):
    if request.method == 'POST':
        form_manga = MangaForm(request.POST or None, request.FILES)
        if form_manga.is_valid():
            manga = form_manga.save(commit=False)
            manga.created_by = request.user
            manga.save()
            messages.success(request,"Manga added!")

            return redirect(reverse("home:home"))
    else:
        form_manga = MangaForm()

    context = {
        "form_manga" : form_manga
    }

    return render(request, "pages/manga_add.html", context)

def genre_add(request):
    if request.method == 'POST':
        form_genre = GenreForm(request.POST or None)
        if form_genre.is_valid():
            form_genre.save()
            return redirect("home:home")
        else:
            print("falhou")

    else:
        form_genre = GenreForm()

    context = {
        "form_genre" : form_genre
    }

    return render(request, "pages/genre_add.html", context)