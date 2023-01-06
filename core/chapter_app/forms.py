from django import forms
from .models import Chapter, Page
from manga_app.models import Manga

class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = '__all__'

class ChapterForm(forms.ModelForm):
    
    class Meta:
        model = Chapter
        fields = ['name_chapter','manga']

    def __init__(self, *args, **kwargs):
        self.fields['manga'].queryset = Manga.objects.all()