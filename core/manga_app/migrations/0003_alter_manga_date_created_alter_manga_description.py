# Generated by Django 4.1.4 on 2023-01-02 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga_app', '0002_alter_manga_cover_alter_manga_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='date_created',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='manga',
            name='description',
            field=models.TextField(),
        ),
    ]
