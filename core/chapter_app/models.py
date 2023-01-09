from django.db import models
from uuid import uuid4
from manga_app.models import Manga
from django.contrib.auth import settings
from django.db.models import F

# Create your models here.


class Chapter(models.Model):
    id_chapter = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name_chapter = models.CharField(max_length=300)
    manga = models.ForeignKey(Manga,on_delete=models.CASCADE, null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)


    class Meta:
        verbose_name_plural = "Chapters"
        ordering = [F('name_chapter').asc(nulls_last=True)]
        permissions = [('can_add_chapter', 'Can add chapter'),
                       ('can_delete_chapter', 'Can delete chapter'),
                       ('can_edit_chapter', 'Can edit chapter'),
                       ('can_view_chapter', 'Can view chapter')]
    def __str__(self):
        return self.name_chapter

    def __unicode__(self):
        return self.name_chapter

class Page(models.Model):
    id_img = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    image_chapter = models.URLField(max_length=900)
    chapter_name = models.ForeignKey(Chapter,on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)


    class Meta:
        verbose_name_plural = "Pages"
        ordering = [F('image_chapter').asc(nulls_last=True)]
        permissions = [('can_add_page', 'Can add page'),
                       ('can_delete_page', 'Can delete page'),
                       ('can_edit_page', 'Can edit page'),
                       ('can_view_page', 'Can view page')]

    def __str__(self):
        return f'Page of {self.chapter_name.name_chapter}'

    def __unicode__(self):
        return self.chapter_name.name_chapter