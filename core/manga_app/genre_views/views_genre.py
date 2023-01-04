from django.shortcuts import render, redirect, get_object_or_404
from manga_app.forms import GenreForm
from manga_app.models import Genre
from django.contrib import messages


def genre_list(request):
    genre = Genre.objects.filter(create_by=request.user)
    context = {
        "genres":genre
    }

    return render(request,"pages/genre/genre_list.html",context)

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

    return render(request, "pages/genre/genre_add.html", context)

def genre_edit(request, pk):
    genre = get_object_or_404(Genre, id_genre=pk)
    form_genre = GenreForm(instance=genre)

    if request.method == 'POST':
        form_genre = GenreForm(request.POST or None)
        if form_genre.is_valid():
            gen = form_genre.save(commit=False)
            gen.create_by = request.user
            gen.save()
            messages.success(request, "Genre updated!")
            return redirect('manga:genre_list')
    context = {
        'form_genre' : form_genre
    }

    return render(request,"pages/genre/genre_edit.html", context)

def genre_delete(request, pk):
    genre = get_object_or_404(Genre, id_genre=pk)
    genre.delete()
    messages.success(request, 'Genre deleted!')

    return redirect('manga:genre_list')
