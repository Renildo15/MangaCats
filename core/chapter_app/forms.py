from django import forms
from .models import Chapter, Page


class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = '__all__'

class ChapterForm(forms.ModelForm):

    class Meta:
        model = Chapter
        fields = '__all__'