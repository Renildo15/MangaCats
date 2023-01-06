from django.shortcuts import render
from .models import Chapter, Page
# Create your views here.

#Todo: Sistema de avaliação(adicionar no model de manga_app)
#Todo: Adicionar campo para salvar mangá favorito
#Todo: Adicionar campo de idioma para filtrar mangás por idioma
#TODO: Add campo de imagem para o user

def page_list(request, pk):
    page = Page.objects.filter(chapter_name=pk)

    context = {
        'pages': page
    }

    return render(request, "pages/page_list.html", context)


def chapter_list(request, pk):
    chapter = Chapter.objects.filter(created_by=request.user, manga_id=pk)
    name_list =[]
    img_list = []
    
    if chapter.exists():
        for c in chapter:
            name_list.append(c.manga)
            img_list.append(c.manga.cover)
    
        name_manga = name_list[0]
        manga_cover = img_list[0]
        context = {
            "chapters": chapter,
            "name_manga": name_manga,
            "manga_cover": manga_cover
        }
    else:
        context = {
            "chapters": chapter,
        }

    return render(request, "pages/chapter_list.html", context)