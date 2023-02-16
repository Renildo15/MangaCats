from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from manga_app.forms import GenreForm
from manga_app.models import Genre, Manga
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required


def language(request,queryset):
    laguage_pt = request.GET.get('PT-BR')
    laguage_jp = request.GET.get('JP')
    laguage_eng = request.GET.get('ENG')
    laguage_all = request.GET.get('ALL')

    manga = queryset.all()

    if laguage_eng:
        manga = queryset.filter(language=laguage_eng)
        return manga
    elif laguage_pt: 
        manga = queryset.filter(language=laguage_pt)
        return manga
    elif laguage_jp:
        manga = queryset.filter(language=laguage_jp)
        return manga
    elif laguage_all:
        manga = queryset.all()
        return manga
    
    return manga


def genre(request):
    genre = Genre.objects.all()
    genre_id = genre.values_list('id_genre', flat=True)

    context = {
        "genres": genre,
    }

    return render(request, "pages/genre/genre.html", context)


def genre_filter(request, pk, name_genre):
    manga = Manga.objects.filter(genre=pk)
    manga = language(request, manga)
    manga_total = manga.count()
    context = {
        "mangas": manga,
        "manga_total":manga_total,
        "name_genre":name_genre
    }
    return render(request, "pages/genre/genre_manga.html", context)
   

@login_required(login_url='user:login')
@permission_required('manga_app.view_genre', login_url='user:login')
def genre_list(request):
    genre = Genre.objects.filter(create_by=request.user)
    context = {
        "genres":genre
    }

    return render(request,"pages/genre/genre_list.html",context)


@login_required(login_url='user:login')
@permission_required('manga_app.add_genre', login_url='user:login')
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


@login_required(login_url='user:login')
@permission_required('manga_app.change_genre', login_url='user:login')
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


@login_required(login_url='user:login')
@permission_required('manga_app.delete_genre', login_url='user:login')
def genre_delete(request, pk):
    genre = get_object_or_404(Genre, id_genre=pk)
    genre.delete()
    messages.success(request, 'Genre deleted!')

    return redirect('manga:genre_list')
