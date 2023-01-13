from django import forms
from .models import CommentChapter, CommentManga, ReplyCommentChapter, ReplyCommentManga


class ReplyChapter(forms.ModelForm):

    class Meta:
        model = ReplyCommentChapter
        fields = '__all__'

class ReplyManga(forms.ModelForm):

    class Meta:
        model = ReplyCommentManga
        fields = '__all__'

class CommentChapterForm(forms.ModelForm):

    class Meta:
        model = CommentChapter
        fields = '__all__'



class CommentMangaForm(forms.ModelForm):

    class Meta:
        model = CommentManga
        fields = '__all__'