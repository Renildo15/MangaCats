from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def register_user(request):
    if request.method == "POST":
        form_user = UserCreationForm(request.POST)
        if form_user.is_valid():
            form_user.save()
            return redirect("/")
    else:
        form_user = UserCreationForm()
    context = {
        "form_user" : form_user
    }
    return render(request, "pages/register_user.html", context)