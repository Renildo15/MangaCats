from django import forms
from .models import Manga, Genre, FavoriteManga, ReviewManga

class ReviewMangaForm(forms.ModelForm):
    class Meta:
        model = ReviewManga
        fields = '__all__'


class FavoriteMangaForm(forms.ModelForm):
    class Meta:
        model = FavoriteManga
        fields = '__all__'

        
class MangaForm(forms.ModelForm):
    class Meta:
        model = Manga
        fields = '__all__'
        exclude = ['create_by']

    genre = forms.ModelMultipleChoiceField(
        queryset=None,
        widget = forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request") # store value of request 
        super(MangaForm, self).__init__(*args, **kwargs)
        self.fields['genre'].queryset = Genre.objects.filter(create_by=self.request.user)


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'