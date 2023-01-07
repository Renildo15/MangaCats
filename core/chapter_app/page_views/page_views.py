from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from ..models import Chapter, Page
from ..forms import PageForm, ChapterForm
from manga_app.models import Manga
from django.contrib import messages


def page_list(request, pk):
    page = Page.objects.filter(chapter_name=pk)

    context = {
        'pages': page
    }

    return render(request, "pages/page/page_list.html", context)


def page_add(request, pk):
    form_page = PageForm()
    chapter = get_object_or_404(Chapter, id_chapter=pk)
    form_page['chapter_name'].queryset = Chapter.objects.filter(created_by=request.user)

    if request.method == "POST":
        form_page = PageForm(request.POST or None, request.FILES)
        if form_page.is_valid():
            page = form_page.save(commit=False)
            page.created_by = request.user
            page.chapter_name = chapter
            page.save()
            messages.success(request, f"Page added in {chapter}")
        else:
            print("Invalid")
    else:
        form_page = PageForm()

    context = {
        "form_page": form_page
    }

    return render(request, "pages/page/page_add.html", context)