# Generated by Django 4.1.4 on 2023-01-24 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga_app', '0018_manga_updated_at_alter_manga_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='cover',
            field=models.URLField(max_length=900),
        ),
    ]
