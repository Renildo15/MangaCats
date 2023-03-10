# Generated by Django 4.1.4 on 2023-01-01 20:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='cover',
            field=models.ImageField(upload_to='uploads'),
        ),
        migrations.AlterField(
            model_name='manga',
            name='views',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9000000)]),
        ),
    ]
