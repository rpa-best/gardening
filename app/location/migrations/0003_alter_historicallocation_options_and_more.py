# Generated by Django 4.1 on 2024-03-27 05:25

from django.db import migrations, models
import location.models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_remove_historicallocation_point_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicallocation',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Локация', 'verbose_name_plural': 'historical Локации'},
        ),
        migrations.AlterModelOptions(
            name='historicaluserinlocation',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Пользователи и заявки', 'verbose_name_plural': 'historical Пользователи и заявки'},
        ),
        migrations.AlterModelOptions(
            name='inviteuuid',
            options={'verbose_name': 'Инвайт', 'verbose_name_plural': 'Инвайти'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'Локация', 'verbose_name_plural': 'Локации'},
        ),
        migrations.AlterModelOptions(
            name='userinlocation',
            options={'verbose_name': 'Пользователи и заявки', 'verbose_name_plural': 'Пользователи и заявки'},
        ),
        migrations.AddField(
            model_name='historicaluserinlocation',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('admin', 'Amdin')], default='user', max_length=255),
        ),
        migrations.AddField(
            model_name='userinlocation',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('admin', 'Amdin')], default='user', max_length=255),
        ),
        migrations.AlterField(
            model_name='inviteuuid',
            name='expires_at',
            field=models.DateTimeField(default=location.models.invite_expires_at),
        ),
    ]