# Generated by Django 4.1 on 2024-03-27 11:38

import car.validators
import core.utils.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0002_alter_car_options_alter_historicalcar_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='number',
            field=core.utils.fields.StrippingCharField(max_length=255, validators=[car.validators.car_number_validator]),
        ),
        migrations.AlterField(
            model_name='historicalcar',
            name='number',
            field=core.utils.fields.StrippingCharField(max_length=255, validators=[car.validators.car_number_validator]),
        ),
    ]
