# Generated by Django 3.0.7 on 2020-06-12 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ghumakkad', '0016_sd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='photo',
            field=models.ImageField(upload_to='blog'),
        ),
    ]