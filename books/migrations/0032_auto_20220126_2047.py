# Generated by Django 3.1.7 on 2022-01-26 20:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0031_users_stars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating_star_system',
            name='num_1',
            field=models.SmallIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='rating_star_system',
            name='num_2',
            field=models.SmallIntegerField(blank=True, default=2, null=True),
        ),
        migrations.AlterField(
            model_name='rating_star_system',
            name='num_3',
            field=models.SmallIntegerField(blank=True, default=3, null=True),
        ),
        migrations.AlterField(
            model_name='rating_star_system',
            name='num_4',
            field=models.SmallIntegerField(blank=True, default=4, null=True),
        ),
        migrations.AlterField(
            model_name='rating_star_system',
            name='num_5',
            field=models.SmallIntegerField(blank=True, default=5, null=True),
        ),
        migrations.AlterField(
            model_name='users_stars',
            name='stars',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='users_stars',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
