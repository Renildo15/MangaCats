# Generated by Django 4.1.4 on 2023-02-15 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga_app', '0023_alter_manga_num_chapter'),
    ]

    operations = [
        migrations.AddField(
            model_name='manga',
            name='update_type',
            field=models.CharField(choices=[('views', 'Views'), ('content', 'Content')], default='content', max_length=100),
        ),
    ]
