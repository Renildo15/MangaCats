# Generated by Django 4.1.4 on 2023-01-09 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga_app', '0012_alter_genre_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='manga',
            name='favorite_manga',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='manga',
            name='language',
            field=models.CharField(choices=[('ENG', 'English'), ('PT-BR', 'Português'), ('JP', '日本語')], default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manga',
            name='review',
            field=models.CharField(blank=True, choices=[('M', 'Masterpiece'), ('G', 'Good'), ('A', 'Average'), ('B', 'Bad'), ('H', 'Horrible')], max_length=200, null=True),
        ),
    ]
