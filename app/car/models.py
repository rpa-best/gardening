from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from rest_framework.exceptions import ValidationError
from core.utils.fields import StrippingCharField
from .validators import car_number_validator

User = get_user_model()

class Car(models.Model):
    user = models.ForeignKey(User, models.CASCADE, verbose_name = "Пользователь")
    model = models.CharField(max_length=255, verbose_name = "Марка")
    number = StrippingCharField(max_length=255, validators=[car_number_validator], verbose_name = "Номер")

    history = HistoricalRecords()

    class Meta:
        unique_together = (("user", "number"),)
        verbose_name = "Машина"
        verbose_name_plural = "Машини"
    
    def __str__(self) -> str:
        return f'{self.number} ({self.user})'

    @classmethod
    def add_car(cls, user: User, **kwargs):
        if Car.objects.filter(user=user).count() + 1 > user.max_cars_count:
            raise ValidationError(_("Cars crowed"), "cars_crowded_to_user")
        return cls.objects.create(user=user, **kwargs)
