from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from ..models import Chapter, Page
from ..forms import PageForm, ChapterForm
from comment_app.forms import CommentChapterForm, CommentMangaForm
from manga_app.models import Manga
from django.contrib import messages
from comment_app.comment_chapter.views import comment_chapter_list


def page_list(request, pk):
    page = Page.objects.filter(chapter_name=pk)
    comment_chapter = comment_chapter_list(pk)
    chapter = Chapter.objects.get(id_chapter=pk)
    form_comment = CommentChapterForm()
    if request.method == "POST":
        if request.user.is_authenticated:
            form_comment = CommentChapterForm(request.POST or None)
            if form_comment.is_valid():
                comment = form_comment.save(commit = False)
                comment.user = request.user
                comment.chapter = chapter
                comment.save()
                messages.success(request, "Comment successfully added!")
                return HttpResponseRedirect(reverse("chapter:page_list", args=(pk,))) 
            else:
                print("Invalid")
        else:
            messages.warning(request, "You must be logged in to comment!")
    else:
        form_comment = CommentMangaForm()
    
    context = {
        'pages': page,
        'comments': comment_chapter,
        'form_comment':form_comment
    }

    return render(request, "pages/page/page_list.html", context)


@permission_required({("page.add_page"), "page.can_add_page"}, login_url='user:login')
@login_required(login_url='user:login')
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
            return redirect(reverse("chapter:page_add", args=(pk,)))
        else:
            print("Invalid")
    else:
        form_page = PageForm()

    context = {
        "form_page": form_page
    }

    return render(request, "pages/page/page_add.html", context)


@permission_required({("page.view_page"), "page.can_view_page"}, login_url='user:login')
@login_required(login_url='user:login')
def page_list_manager(request, pk):
    page = Page.objects.filter(chapter_name=pk, created_by=request.user)
    context = {
        "pages": page
    }

    return render(request, "pages/page/page_list_manager.html", context)

@permission_required({("page.change_page"), "page.can_edit_page"}, login_url='user:login')
@login_required(login_url='user:login')
def page_edit(request, pk):
    page = get_object_or_404(Page, id_img=pk)
    form_page = PageForm(instance=page)

    if request.method == "POST":
        form_page = PageForm(request.POST or None, request.FILES, instance=page)
        form_page.fields['chapter_name'].queryset = Chapter.objects.filter(created_by=request.user)

        if form_page.is_valid():
            p = form_page.save(commit=False)
            p.created_by = request.user
            p.save()
            messages.success(request,"Page edited!")
            return redirect(reverse("chapter:page_list_manager", args=(page.chapter_name.id_chapter,)))

    context = {
        "form_page": form_page
    }

    return render(request, "pages/page/page_edit.html", context)

@permission_required({("page.delete_page"), "page.can_delete_page"}, login_url='user:login')
@login_required(login_url='user:login')
def page_delete(request,pk):
    page = Page.objects.get(id_img=pk)
    page.delete()
    messages.success(request,"Page deleted!")
    return redirect(reverse("chapter:page_list_manager", args=(page.chapter_name.id_chapter,)))