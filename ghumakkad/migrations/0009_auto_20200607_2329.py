# Generated by Django 3.0.7 on 2020-06-07 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ghumakkad', '0008_auto_20200607_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
