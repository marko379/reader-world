# Generated by Django 3.1.7 on 2022-01-26 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0033_auto_20220126_2247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating_star_system',
            name='num_1',
        ),
        migrations.RemoveField(
            model_name='rating_star_system',
            name='num_2',
        ),
        migrations.RemoveField(
            model_name='rating_star_system',
            name='num_3',
        ),
        migrations.RemoveField(
            model_name='rating_star_system',
            name='num_4',
        ),
        migrations.RemoveField(
            model_name='rating_star_system',
            name='num_5',
        ),
    ]
