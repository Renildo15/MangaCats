from django.shortcuts import render, redirect
from manga_app.forms import GenreForm
from manga_app.models import Genre
from django.contrib import messages


def genre_list(request):
    genre = Genre.objects.filter(create_by=request.user)

    context = {
        "genres":genre
    }

    return render(request,"pages/genre_list.html",context)

def genre_add(request):
    if request.method == 'POST':
        form_genre = GenreForm(request.POST or None)
        if form_genre.is_valid():
            genre = form_genre.save(commit=False)
            genre.create_by = request.user
            genre.save()
            messages.success(request,"Genre added!")
            return redirect("home:home")
    else:
        form_genre = GenreForm()

    context = {
        "form_genre" : form_genre
    }

    return render(request, "pages/genre_add.html", context)