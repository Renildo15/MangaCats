from django.db import models
from uuid import uuid4
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth import settings
from django.db.models import F
# Create your models here.


class Genre(models.Model):
    id_genre = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name_genre = models.CharField(max_length=300)
    date_created = models.DateTimeField(auto_now=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Genres"
        ordering = [F('name_genre').asc(nulls_last=True)]


    def __str__(self):
        return self.name_genre




class Manga(models.Model):
    choice_status = (
        ('Completed',"Completed"),
        ("On going", "On going"),
        ("Pause",("Pause"))
    )

    id_manga = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name_manga = models.CharField(max_length=300)
    name_in_japanese = models.CharField(max_length=300, null=True, blank=True)
    name_in_english = models.CharField(max_length=300, null=True, blank=True)
    num_chapter = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(9000000)], null=True, blank=True)
    cover = models.ImageField(upload_to ='uploads')
    author = models.CharField(max_length=300)
    status = models.CharField(max_length=300, choices=choice_status)
    views_manga = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(9000000)])
    description = models.TextField()
    date_created = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    genre = models.ManyToManyField(Genre, blank=True)

    class Meta:
        verbose_name_plural = "Mangas"
        ordering = ("name_manga",)

    def __str__(self):
        return self.name_manga
