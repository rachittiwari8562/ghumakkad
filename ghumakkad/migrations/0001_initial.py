# Generated by Django 3.0.7 on 2020-06-05 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('lat', models.DecimalField(decimal_places=8, max_digits=20)),
                ('long', models.DecimalField(decimal_places=8, max_digits=20)),
            ],
        ),
    ]