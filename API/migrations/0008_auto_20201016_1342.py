# Generated by Django 3.1.2 on 2020-10-16 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0007_auto_20201016_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=500, verbose_name='Title'),
        ),
    ]
