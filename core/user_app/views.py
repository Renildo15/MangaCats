from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from .forms import RegisterUserForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.db.models.query_utils import Q

# Create your views here.

def register_user(request):
    if request.method == "POST":
        form_user = RegisterUserForm(request.POST)
        if form_user.is_valid():
            form_user.save()
            messages.success(request,("Usuário criado com sucesso!"))
            return redirect("user:login")
    else:
        form_user = RegisterUserForm()
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


def change_password(request):
    if request.method == "POST":
        form_password = PasswordChangeForm(request.user, request.POST)
        if form_password.is_valid():
            user = form_password.save()
            update_session_auth_hash(request, user)
            messages.success(request,("Senha alterada com sucesso!"))
            return redirect("/")
    else:
        form_password = PasswordChangeForm(request.user)

    context = {
        "form_password" : form_password
    }

    return render(request, "pages/change_password.html", context)

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "senha/password_reset_email.txt"
                    c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/auth/reset_password_sent/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="pages/password/password_reset.html", context={"password_reset_form":password_reset_form})