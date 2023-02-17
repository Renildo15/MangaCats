from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from .forms import RegisterUserForm, EmailAuthenticationForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.

def register_user(request):
    if request.method == "POST":
        form_user = RegisterUserForm(request.POST)
        if form_user.is_valid():
            user = form_user.save(commit=False)
            user.save()
            user_group = Group.objects.get(name='user-logado') 

            user.groups.add(user_group)
            messages.success(request,("User successfully created!"))
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
            messages.success(request,(f"Welcome, {request.user}"))
            return redirect("/")
        else:
            messages.error(request, "Login failed. Please check your email and password.")
            form_login = EmailAuthenticationForm()
    else:
        form_login = EmailAuthenticationForm()

    context = {
        "form_login": form_login,
    }

    return render(request, "pages/login.html", context)

@login_required(login_url='user:login')
def logout_user(request):
    logout(request)
    messages.success(request,("Logged out user"))
    return redirect("/")

@login_required(login_url='user:login')
def change_password(request):
    if request.method == "POST":
        form_password = PasswordChangeForm(request.user, request.POST)
        if form_password.is_valid():
            user = form_password.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse("user:account"))
    else:
        form_password = PasswordChangeForm(request.user)

    return form_password
    
@login_required(login_url='user:login')
def change_password_success(request):
    return render(request, 'pages/password/password_reset_complete.html')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "pages/password/password_reset_email.txt"
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