# Generated by Django 4.1.4 on 2023-01-01 20:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id_genre', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name_genre', models.CharField(max_length=300)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('create_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Genres',
                'ordering': [models.OrderBy(models.F('name_genre'), nulls_last=True)],
            },
        ),
        migrations.CreateModel(
            name='Manga',
            fields=[
                ('id_manga', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name_manga', models.CharField(max_length=300)),
                ('name_in_japanese', models.CharField(blank=True, max_length=300, null=True)),
                ('name_in_english', models.CharField(blank=True, max_length=300, null=True)),
                ('cover', models.ImageField(upload_to='uploads/% Y/% m/% d/')),
                ('author', models.CharField(max_length=300)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('On going', 'On going'), ('Pause', 'Pause')], max_length=300)),
                ('views', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('description', models.TextField(max_length=800)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('create_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('genre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manga_app.genre')),
            ],
            options={
                'verbose_name_plural': 'Mangas',
                'ordering': [models.OrderBy(models.F('name_manga'), nulls_last=True)],
            },
        ),
    ]
