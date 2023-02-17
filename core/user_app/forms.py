from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from django.forms import ImageField, FileInput, EmailInput


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.EmailInput(attrs={'type': 'email'}), label="Email")

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].label = "Email"

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(), label="Email")
    first_name = forms.CharField(widget=forms.TextInput(), label="First name")
    last_name = forms.CharField(widget=forms.TextInput(), label="Last name")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class PasswordChangingForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        exclude = ['password']

class ProfileAvatarForm(forms.ModelForm):
    #esconde o imagge currently
    image_profile = ImageField(widget=FileInput)
    class Meta:
        model = Profile
        fields = ('image_profile',)
        exclude = ['user', 'date_created']
