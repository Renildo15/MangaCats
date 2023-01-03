from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Manga
from .forms import MangaForm
from django.contrib import messages
# Create your views here.

def manga_list(request):
    manga = Manga.objects.all()
    context = {
        "mangas": manga
    }
    return render(request,"pages/manga/manga_list.html", context)


def manga_uploaded(request):
    manga = Manga.objects.filter(create_by=request.user)
    context = {
        "mangas": manga
    }
    return render(request,"pages/manga/manga_uploaded.html", context)

def manga_view(request, pk):
    manga = Manga.objects.get(id_manga=pk)

    context = {
        "manga": manga
    }

    return render(request, "pages/manga/manga_view.html", context)

def manga_add(request):
    if request.method == 'POST':
        form_manga = MangaForm(request.POST or None, request.FILES)
        if form_manga.is_valid():
            manga = form_manga.save(commit=False)
            manga.create_by = request.user
            manga.save()
            messages.success(request,"Manga added!")

            return redirect(reverse("home:home"))
    else:
        form_manga = MangaForm()

    context = {
        "form_manga" : form_manga
    }

    return render(request, "pages/manga/manga_add.html", context)

def manga_edit(request, pk):
    manga = get_object_or_404(Manga, id_manga=pk)
    form_manga = MangaForm(instance=manga)
    if request.method == "POST":
        form_manga = MangaForm(request.POST or None, request.FILES, instance=manga)
        if form_manga.is_valid():
            manga = form_manga.save(commit=False)
            manga.create_by = request.user
            manga.save()
            messages.success(request, f"Manga {manga.name_manga} updated!")
            return redirect('manga:manga_uploaded')
    elif(request.method == 'GET'):
         return render(request, "pages/manga/manga_edit.html", {'form_manga': form_manga})

    return render(request, "pages/manga/manga_edit.html", {'form_manga': form_manga})
