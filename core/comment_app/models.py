from django.db import models
from uuid import uuid4
from manga_app.models import Manga
from chapter_app.models import Chapter
from django.contrib.auth import settings
from tinymce.models import HTMLField
# Create your models here.


class CommentManga(models.Model):
    id_comment = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    comment = HTMLField()
    date_created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    manga = models.ForeignKey(Manga, null=True, blank=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, blank=True, related_name='replies')
    

    class Meta:
        verbose_name_plural = "Comments Manga"
        ordering = ['-date_created']
     

    def __str__(self):
        return f'{self.user} - {self.comment}'


class CommentChapter(models.Model):
    id_comment = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    comment = HTMLField()
    date_created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    chapter = models.ForeignKey(Chapter, null=True, blank=True, on_delete=models.CASCADE)
    

    class Meta:
        verbose_name_plural = "Comments Chapters"
        ordering = ['-date_created']
        
    def __str__(self):
        return f'{self.user} - {self.comment}'



   
