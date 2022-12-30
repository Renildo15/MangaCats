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
            messages.success(request,("Usuário criado com sucesso!"))
            return redirect("user:login")
    else:
        form_user = UserCreationForm()
    context = {
        "form_user" : form_user
    }
    return render(request, "pages/register_user.html", context)

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,(f"Seja bem vindo {request.user}"))
            return redirect("/")
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()

    context = {
        "form_login": form_login
    }

    return render(request, "pages/login.html", context)



def logout_user(request):
    logout(request)
    messages.success(request,("Usuário deslogado"))
    return redirect("/")