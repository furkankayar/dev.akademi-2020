# Generated by Django 3.1.2 on 2020-10-16 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_auto_20201016_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=2000, verbose_name='Description'),
        ),
    ]