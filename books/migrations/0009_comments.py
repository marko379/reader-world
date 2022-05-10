# Generated by Django 3.1.7 on 2022-01-02 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_book_genres'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='books.book')),
            ],
        ),
    ]
