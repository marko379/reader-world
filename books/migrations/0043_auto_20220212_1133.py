# Generated by Django 3.1.7 on 2022-02-12 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0042_auto_20220202_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.TextField(blank=True, max_length=30000, null=True),
        ),
    ]
