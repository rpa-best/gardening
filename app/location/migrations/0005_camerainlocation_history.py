# Generated by Django 4.1 on 2024-03-27 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('car', '0001_initial'),
        ('camera', '0001_initial'),
        ('location', '0004_carinlocation_blocked_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CameraInLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mode', models.CharField(choices=[('in', 'Вход'), ('out', 'Выход')], max_length=255)),
                ('camera', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='camera.camera')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.location')),
            ],
            options={
                'verbose_name': 'Камера в локации',
                'verbose_name_plural': 'Камеры в локации',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('car_number', models.CharField(max_length=255)),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='car.car')),
                ('car_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('cil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.camerainlocation')),
            ],
            options={
                'verbose_name': 'История локации',
                'verbose_name_plural': 'Истории локации',
            },
        ),
    ]
