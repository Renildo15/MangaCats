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
        permissions = [('can_add_genre', 'Can add genre'),
                       ('can_delete_genre', 'Can delete genre'),
                       ('can_edit_genre', 'Can edit genre'),
                       ('can_view_genre', 'Can view genre')]


    def __str__(self):
        return self.name_genre




class Manga(models.Model):
    choice_status = (
        ('Completed',"Completed"),
        ("On going", "On going"),
        ("Pause",("Pause"))
    )

    
    choice_languages = (
        ('ENG', "English"),
        ("PT-BR", "Português"),
        ("JP", "日本語")
    )

    id_manga = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name_manga = models.CharField(max_length=300)
    name_in_japanese = models.CharField(max_length=300, null=True, blank=True)
    name_in_english = models.CharField(max_length=300, null=True, blank=True)
    language = models.CharField(max_length=200, choices=choice_languages)
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
        permissions = [('can_add_manga', 'Can add manga'),
                       ('can_delete_manga', 'Can delete manga'),
                       ('can_edit_manga', 'Can edit manga'),
                       ('can_view_manga', 'Can view manga')]

    def __str__(self):
        return self.name_manga

    def __unicode__(self):
        return self.name_manga


class FavoriteManga(models.Model):
    id_favorite = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    favorite_manga = models.BooleanField(default=False, null=True, blank=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Favorites Manga"
        ordering = ("favorite_manga",)

    def __str__(self):
        return f'User: {self.user.username}-favorite manga: {self.manga.name_manga}'


class ReviewManga(models.Model):
    choice_review = (
        (1, "Horrible"),
        (2, "Bad"),
        (3, "Average"),
        (4, "Good"),
        (5, "Masterpiece")
    )
    id_review = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    review = models.IntegerField(choices=choice_review)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Reviews Manga"
        ordering = ("review",)

    def __str__(self):
        return f'User: {self.user.username}-favorite manga: {self.manga.name_manga} - Review: {self.review}'