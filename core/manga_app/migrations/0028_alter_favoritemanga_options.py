# Generated by Django 4.1.4 on 2023-02-18 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manga_app', '0027_alter_favoritemanga_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoritemanga',
            options={'ordering': ('favorite_manga',), 'verbose_name_plural': 'Favorites Manga'},
        ),
    ]
