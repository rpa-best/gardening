from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from rest_framework.exceptions import ValidationError
from .validators import car_number_validator

User = get_user_model()

class Car(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    model = models.CharField(max_length=255)
    number = models.CharField(max_length=255, validators=[car_number_validator])

    history = HistoricalRecords()

    class Meta:
        unique_together = (("user", "number"),)

    @classmethod
    def add_car(cls, user: User, **kwargs):
        if Car.objects.filter(user=user).count() + 1 > user.max_cars_count:
            raise ValidationError(_("Cars crowed"), "cars_crowded_to_user")
        return cls.objects.create(user=user, **kwargs)