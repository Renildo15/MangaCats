# Generated by Django 4.1.4 on 2023-01-04 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga_app', '0011_alter_manga_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': [models.OrderBy(models.F('name_genre'), nulls_last=True)], 'permissions': [('can_add_genre', 'Can add genre'), ('can_delete_genre', 'Can delete genre'), ('can_edit_genre', 'Can edit genre'), ('can_view_genre', 'Can view genre')], 'verbose_name_plural': 'Genres'},
        ),
    ]
