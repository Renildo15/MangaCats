from django.shortcuts import render
from .models import Chapter, Page
# Create your views here.

def page_list(request, pk):
    page = Page.objects.filter(chapter_name=pk)

    context = {
        'pages': page
    }

    return render(request, "pages/page_list.html", context)
