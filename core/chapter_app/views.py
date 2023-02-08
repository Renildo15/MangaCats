from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from .models import Chapter, Page
from .forms import PageForm, ChapterForm
from manga_app.models import Manga
from django.contrib import messages
# Create your views here.

@permission_required({("chapter.view_chapter"), "chapter.can_view_chapter"}, login_url='user:login')
@login_required(login_url='user:login')
def chapter_list(request, pk):
    chapter = Chapter.objects.filter(created_by=request.user, manga_id=pk)
    name_list =[]
    img_list = []
    id_list = []
    
    if chapter.exists():
        for c in chapter:
            name_list.append(c.manga)
            img_list.append(c.manga.cover)
            id_list.append(c.manga.id_manga)
    
        name_manga = name_list[0]
        manga_cover = img_list[0]
        manga_id = id_list[0]
        context = {
            "chapters": chapter,
            "name_manga": name_manga,
            "manga_cover": manga_cover,
            "manga_id": manga_id
        }
    else:
        context = {
            "chapters": chapter,
            "manga_id": pk
        }

    return render(request, "pages/chapter/chapter_list.html", context)

@permission_required({("chapter.add_chapter"), "chapter.can_add_chapter"}, login_url='user:login')
@login_required(login_url='user:login')
def chapter_add(request, pk):
    manga = get_object_or_404(Manga, id_manga=pk)
    if request.method == "POST":
        form_chapter = ChapterForm(request.POST or None)

        if form_chapter.is_valid():
            chapter = form_chapter.save(commit=False)
            chapter.manga = manga
            chapter.created_by = request.user
            chapter.save()
            messages.success(request, f"{manga.name_manga} - Chapter added!")
            return redirect(reverse("home:home"))
        else:
            print("Invalid")
    else:
        form_chapter = ChapterForm()
        form_chapter['manga'].field.queryset = Manga.objects.filter(create_by=request.user)
        form_chapter['manga'].initial = manga

    context = {
        "form_chapter": form_chapter,
        "manga": manga
    }

    return render(request, "pages/chapter/chapter_add.html", context)

@permission_required({("chapter.change_chapter"), "chapter.can_edit_chapter"}, login_url='user:login')
@login_required(login_url='user:login')
def chapter_edit(request, pk):
    chapter = get_object_or_404(Chapter, id_chapter=pk)
    form_chapter = ChapterForm(instance=chapter)
    form_chapter.fields['manga'].queryset = Manga.objects.filter(create_by=request.user)
    if request.method == "POST":
        form_chapter = ChapterForm(request.POST or None,instance=chapter)
        if form_chapter.is_valid():
            chapter = form_chapter.save(commit=False)
            chapter.created_by = request.user
            chapter.save()
            messages.success(request, f"{chapter.manga} - Chapter edited!")
            return redirect(reverse("manga:manga_uploaded"))
    
    context = {
        "form_chapter": form_chapter
    }

    return render(request, "pages/chapter/chapter_edit.html",context)

@permission_required({("chapter.delete_chapter"), "chapter.can_delete_chapter"}, login_url='user:login')
@login_required(login_url='user:login')
def chapter_delete(request, pk):
    chapter = Chapter.objects.get(id_chapter=pk)
    chapter.delete()
    messages.success(request, f"{chapter.manga} - Chapter deleted!")
    return redirect(reverse("manga:manga_uploaded"))