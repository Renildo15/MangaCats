# Generated by Django 4.1.4 on 2023-01-10 17:20

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('comment_app', '0002_alter_commentchapter_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmanga',
            name='comment',
            field=tinymce.models.HTMLField(),
        ),
    ]
