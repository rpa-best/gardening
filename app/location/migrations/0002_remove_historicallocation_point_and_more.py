# Generated by Django 4.1 on 2024-03-26 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicallocation',
            name='point',
        ),
        migrations.RemoveField(
            model_name='location',
            name='point',
        ),
    ]