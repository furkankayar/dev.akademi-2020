# Generated by Django 3.1.2 on 2020-10-16 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0006_auto_20201016_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=20000, verbose_name='Description'),
        ),
    ]