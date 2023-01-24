from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from ..forms import ProfileAvatarForm, ProfileUserForm
from django.contrib import messages

@login_required(login_url='user:login')
def account(request):
    form_user = ProfileUserForm(instance=request.user)
    form_avatar = ProfileAvatarForm(instance=request.user.profile)
    if request.method == "POST":
        form_user = ProfileUserForm(request.POST or None, instance=request.user)
        form_avatar = ProfileAvatarForm(request.POST or None, request.FILES, instance=request.user.profile)
        if form_user.is_valid():
            form_user.save()
            messages.success(request, "User updated!")
            return HttpResponseRedirect(reverse("user:account")) 
        else:
            print("invalid")

        if form_avatar.is_valid():
            form_avatar.save()
            messages.success(request, "Avatar updated!")
            return HttpResponseRedirect(reverse("user:account")) 
            
    context = {
        "form_user":form_user,
        "form_avatar":form_avatar
    }
    return render(request, "pages/profile/profile_page.html",context)

def profile_update(request):
    pass