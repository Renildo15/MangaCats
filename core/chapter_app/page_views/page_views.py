from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from ..models import Chapter, Page
from comment_app.models import CommentChapter
from ..forms import PageForm
from comment_app.forms import CommentChapterForm, CommentMangaForm
from manga_app.models import Manga
from django.contrib import messages
from comment_app.comment_chapter.views import comment_chapter_list, total_comments_chapter

def previous_chapter(request, pk, name):
    chapter = Chapter.objects.get(id_chapter=pk)
    previous_chapter = Chapter.objects.filter(name_chapter__lt=name,manga=chapter.manga).order_by("-name_chapter").first()
    
    if previous_chapter:
        return redirect("chapter:page_list",str(previous_chapter.id_chapter))

    return redirect("chapter:page_list",pk)

def next_chapter(request, pk, name):
    chapter = Chapter.objects.get(id_chapter=pk)
    next_chapter = Chapter.objects.filter(name_chapter__gt=name,manga=chapter.manga).order_by("name_chapter").first()
    print(next_chapter)
    if next_chapter:
        return redirect("chapter:page_list",str(next_chapter.id_chapter))
    return redirect("chapter:page_list",pk)

def page_list(request, pk):
    page = Page.objects.filter(chapter_name=pk)
    comment_chapter = comment_chapter_list(request,pk)
    chapter = Chapter.objects.get(id_chapter=pk)
    form_comment = CommentChapterForm()
    total_comments = total_comments_chapter(pk)
    manga_chapters = Chapter.objects.filter(manga=chapter.manga)

    if request.method == "POST":
        if request.user.is_authenticated:
            form_comment = CommentChapterForm(request.POST or None)
            if form_comment.is_valid():
                parent_obj = None
                try:
                    parent_id = request.POST.get('parent_id')
                except:
                    parent_id = None

                if parent_id:
                    parent_obj = CommentChapter.objects.get(id_comment=parent_id)
                    if parent_obj:
                        replay_comment = form_comment.save(commit=False)
                        replay_comment.parent = parent_obj
                        replay_comment.active = True
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
        'comments': comment_chapter["comment_chapter"],
        "qnt_page":comment_chapter["qnt_page"],
        'form_comment':form_comment,
        'total_comments': total_comments,
        "chapter_id":chapter.id_chapter,
        "chapter_name":chapter.name_chapter,
        "manga_chapters":manga_chapters,
    }

    return render(request, "pages/page/page_list.html", context)


@permission_required({("chapter_app.add_page"), "page.can_add_page"}, login_url='user:login')
@login_required(login_url='user:login')
def page_add(request, pk):
    chapter = get_object_or_404(Chapter, id_chapter=pk)
    if request.method == "POST":
        form = PageForm(request.POST or None, request.FILES)
        if form.is_valid():
            page = form.save(commit=False)
            page.created_by = request.user
            page.chapter_name = chapter
            page.save()
            messages.success(request, f"Page added in {chapter}")
            return redirect(reverse("chapter:page_add", args=(pk,)))
        else:
            print("Invalid")
    else:
        manga = get_object_or_404(Manga, id_manga=chapter.manga.id_manga)
        form = PageForm()
        form['chapter_name'].field.queryset = Chapter.objects.filter(created_by=request.user, manga_id=manga)
        form['chapter_name'].initial = chapter

    context = {
        "form_page": form
    }

    return render(request, "pages/page/page_add.html", context)


@permission_required({("chapter_app.view_page"), "chapter_app.can_view_page"}, login_url='user:login')
@login_required(login_url='user:login')
def page_list_manager(request, pk):
    page = Page.objects.filter(chapter_name=pk, created_by=request.user)
    context = {
        "pages": page
    }

    return render(request, "pages/page/page_list_manager.html", context)

@permission_required({("chapter_app.change_page"), "chapter_app.can_edit_page"}, login_url='user:login')
@login_required(login_url='user:login')
def page_edit(request, pk):
    page = get_object_or_404(Page, id_img=pk)
    if request.method == "POST":
        form_page = PageForm(request.POST or None, request.FILES, instance=page)
        if form_page.is_valid():
            p = form_page.save(commit=False)
            p.created_by = request.user
            p.save()
            messages.success(request,"Page edited!")
            return redirect(reverse("chapter:page_list_manager", args=(page.chapter_name.id_chapter,)))
    else:
        chapter = get_object_or_404(Chapter, id_chapter=page.chapter_name.id_chapter)
        manga = get_object_or_404(Manga, id_manga=chapter.manga.id_manga)
        form_page = PageForm(instance=page)
        form_page['chapter_name'].field.queryset = Chapter.objects.filter(created_by=request.user, manga=manga)
    context = {
        "form_page": form_page
    }

    return render(request, "pages/page/page_edit.html", context)

@permission_required({("chapter_app.delete_page"), "chapter_app.can_delete_page"}, login_url='user:login')
@login_required(login_url='user:login')
def page_delete(request,pk):
    page = Page.objects.get(id_img=pk)
    page.delete()
    messages.success(request,"Page deleted!")
    return redirect(reverse("chapter:page_list_manager", args=(page.chapter_name.id_chapter,)))