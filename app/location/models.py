import datetime
from uuid import uuid4
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.utils import aware_utcnow
from rest_framework import exceptions
from simple_history.models import HistoricalRecords


INVITE_URL = "https://kk.keyman24.ru/invite-location"
INVITE_STATUS_CHECKING = "checking"
INVITE_STATUS_ACCEPTED = "accepted"
INVITE_STATUS = (
    (INVITE_STATUS_CHECKING, "Checking"),
    (INVITE_STATUS_ACCEPTED, "Accepted")
)
ROLE_USER = "user"
ROLE_ADMIN = "admin"
ROLES = (
    (ROLE_USER, "User"),
    (ROLE_ADMIN, "Admin")
)

User = get_user_model()


class Location(models.Model):
    name = models.CharField(max_length=255)
    max_count_cars = models.IntegerField()
    max_count_users = models.IntegerField()
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self) -> str:
        return self.name
    
    def create_invite(self):
        return InviteUUID.create(self)
    
    def add_car(self, car):
        uil = UserInLocation.objects.filter(user=car.user, location=self).first()
        if not uil:
            raise exceptions.ValidationError(_("User of car not added to location"), "user_not_in_location")
        if uil.status in [INVITE_STATUS_CHECKING]:
            raise exceptions.ValidationError(_("Your invite to location not accepted"), "invite_not_accepted")
        if uil.max_count_cars < uil.count_cars + 1:
            raise exceptions.ValidationError(_("Cars crowded to this user"), "cars_crowded_to_user")
        return CarInLocation.objects.create(location=self, car=car)
        
    @property
    def count_cars(self):
        return CarInLocation.objects.filter(location=self).count()
    
    @property
    def accepted_count_users(self):
        return UserInLocation.objects.filter(location=self, status=INVITE_STATUS_ACCEPTED).count()

    @property
    def checking_count_users(self):
        return UserInLocation.objects.filter(location=self, status=INVITE_STATUS_CHECKING).count()


class UserInLocation(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    location = models.ForeignKey(Location, models.CASCADE)
    max_count_cars = models.IntegerField(default=1)
    status = models.CharField(max_length=255, default=INVITE_STATUS_CHECKING, choices=INVITE_STATUS)
    role = models.CharField(max_length=255, choices=ROLES, default=ROLE_USER)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self.user} ({self.location})"

    class Meta:
        verbose_name = "Пользователи и заявки"
        verbose_name_plural = "Пользователи и заявки"
        unique_together = (("user", "location"),)

    @property
    def count_cars(self):
        return CarInLocation.objects.filter(location=self.location, car__user=self.user).count()
    
    def accept(self, **kwargs):
        max_count_cars = kwargs.get("max_count_cars", 1)
        if self.location.accepted_count_users + 1 > self.location.max_count_users:
            raise exceptions.ValidationError(_("Users crowded"), "users_crowded")
        if self.location.count_cars + max_count_cars > self.location.max_count_cars:
            raise exceptions.ValidationError(_("Places crowded"), "places_crowded")
        self.max_count_cars = max_count_cars
        self.status = INVITE_STATUS_ACCEPTED
        self.save()
        return self


class CarInLocation(models.Model):
    location = models.ForeignKey(Location, models.CASCADE)
    car = models.ForeignKey("car.Car", models.CASCADE)
    blocked = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        unique_together = (("car", "location"),)
    
    def __str__(self) -> str:
        return f"{self.car} ({self.car.user})"


def invite_expires_at():
    current_time = aware_utcnow()
    return current_time + InviteUUID.lifetime


class InviteUUID(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    location = models.ForeignKey(Location, models.CASCADE)
    expires_at = models.DateTimeField(default=invite_expires_at)
    lifetime = datetime.timedelta(days=1)

    class Meta:
        verbose_name = "Инвайт"
        verbose_name_plural = "Инвайти"

    @property
    def url(self):
        return f"{INVITE_URL}?uuid={self.uuid}"
    
    def validate(self):
        current_time = aware_utcnow()
        if self.expires_at <= current_time - self.lifetime:
            raise exceptions.ValidationError(_("UUID has expired"), "uuid_expired")
        return self
    
    def accept_invite(self, user: User) -> UserInLocation:
        uil = UserInLocation.objects.create(
            user=user, location=self.location
        )
        self.delete()
        return uil
