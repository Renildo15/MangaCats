# Generated by Django 4.1.4 on 2023-01-17 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment_app', '0014_commentchapter_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentchapter',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
