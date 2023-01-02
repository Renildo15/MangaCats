from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User

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

      