# Generated by Django 4.1.4 on 2023-01-31 13:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga_app', '0022_historymanga'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='num_chapter',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9000000)]),
        ),
    ]
