from django import forms
from .models import Manga, Genre
from django.forms import FileInput

class MangaForm(forms.ModelForm):
    class Meta:
        model = Manga
        fields = '__all__'
       

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'