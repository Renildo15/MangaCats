from django.db import models
from uuid import uuid4
from manga_app.models import Manga
from chapter_app.models import Chapter
from django.contrib.auth import settings
# Create your models here.

class CommentManga(models.Model):
    id_comment = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    manga = models.ForeignKey(Manga, null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        return f'Comentário manga - {self.comment[0:10]}'

class CommentChapter(models.Model):
    id_comment = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    chapter = models.ForeignKey(Chapter, null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        return f'Comentário capítulo - {self.comment[0:10]}'