from django.shortcuts import render

# Create your views here.

def home_page(request):
    context = {
        "teste": "teste"
    }
    return render(request,"pages/home.html", context)