# Generated by Django 4.1.4 on 2023-01-24 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga_app', '0019_alter_manga_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='cover',
            field=models.ImageField(upload_to='uploads'),
        ),
    ]
