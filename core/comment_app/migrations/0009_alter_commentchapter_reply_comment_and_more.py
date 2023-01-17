# Generated by Django 4.1.4 on 2023-01-13 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment_app', '0008_rename_parent_commentchapter_reply_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentchapter',
            name='reply_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies_chapter', to='comment_app.replycommentchapter'),
        ),
        migrations.AlterField(
            model_name='commentmanga',
            name='reply_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies_manga', to='comment_app.replycommentmanga'),
        ),
    ]
