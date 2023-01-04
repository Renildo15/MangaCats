from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='user:login')
def profile_home(request):
    return render(request, "pages/profile.html")