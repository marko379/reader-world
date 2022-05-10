# Generated by Django 3.1.7 on 2022-01-10 18:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0023_rating_star_system_star_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating_star_system',
            name='star_1',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
