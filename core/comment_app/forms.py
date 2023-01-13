from django import forms
from .models import CommentChapter, CommentManga


class CommentChapterForm(forms.ModelForm):

    class Meta:
        model = CommentChapter
        fields = '__all__'



class CommentMangaForm(forms.ModelForm):

    class Meta:
        model = CommentManga
        fields = '__all__'