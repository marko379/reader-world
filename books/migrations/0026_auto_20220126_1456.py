# Generated by Django 3.1.7 on 2022-01-26 14:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0025_auto_20220110_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='comment_dislikes',
            field=models.ManyToManyField(blank=True, related_name='comment_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='comment_likes',
            field=models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='date_comment_modified',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='comments',
            name='date_comment_posted',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
