# Generated by Django 3.1.7 on 2021-12-25 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('writter', models.CharField(max_length=200)),
                ('published', models.CharField(max_length=20)),
                ('pages', models.PositiveSmallIntegerField()),
                ('info', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='books_photos')),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
        ),
    ]
