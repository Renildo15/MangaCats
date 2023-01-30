from django.contrib import admin
from .models import Manga, Genre, FavoriteManga, ReviewManga, StatusManga
# Register your models here.

admin.site.register(Manga)
admin.site.register(Genre)
admin.site.register(FavoriteManga)
admin.site.register(ReviewManga)
admin.site.register(StatusManga)
