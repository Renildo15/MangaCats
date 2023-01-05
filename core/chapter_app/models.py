from django.db import models
from uuid import uuid4
from manga_app.models import Manga
from django.contrib.auth import settings

# Create your models here.


class Chapter(models.Model):
    id_chapeter = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name_chapter = models.CharField(max_length=300)
    manga = models.ForeignKey(Manga,on_delete=models.CASCADE, null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name_chapter

class Page(models.Model):
    id_img = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    image_chapter = models.ImageField(upload_to='uploads/chapters')
    chapter_name = models.ForeignKey(Chapter,on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return f'Page of {self.chapter_name.name_chapter}'