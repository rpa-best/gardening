import datetime
from uuid import uuid4
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.utils import aware_utcnow
from rest_framework import exceptions
from simple_history.models import HistoricalRecords


INVITE_URL = "https://kk.keyman24.ru/api/location/invite"
INVITE_STATUS_CHECKING = "checking"
INVITE_STATUS_ACCEPTED = "accepted"
INVITE_STATUS = (
    (INVITE_STATUS_CHECKING, "На проверке"),
    (INVITE_STATUS_ACCEPTED, "Принята")
)

ROLE_USER = "user"
ROLE_ADMIN = "admin"
ROLES = (
    (ROLE_USER, "Пользователь"),
    (ROLE_ADMIN, "Админ")
)

MODE_IN = "in"
MODE_OUT = "out"
MODES = (
    (None, "Проста камера"),
    (MODE_IN, "Вход"),
    (MODE_OUT, "Выход"),
)

User = get_user_model()


class Location(models.Model):
    name = models.CharField(max_length=255, verbose_name = "Название")
    max_count_cars = models.IntegerField(verbose_name = "Кол-во машин")
    max_count_users = models.IntegerField(verbose_name = "Кол-во пользователи")
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self) -> str:
        return self.name
    
    def create_invite(self):
        return InviteUUID.objects.create(location=self)
    
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
    user = models.ForeignKey(User, models.CASCADE, verbose_name = "Пользователь")
    location = models.ForeignKey(Location, models.CASCADE, verbose_name = "Локация")
    max_count_cars = models.IntegerField(default=1, verbose_name = "Кол-во машин")
    status = models.CharField(max_length=255, default=INVITE_STATUS_CHECKING, choices=INVITE_STATUS, verbose_name = "Статус")
    role = models.CharField(max_length=255, choices=ROLES, default=ROLE_USER, verbose_name = "Роль")
    
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
    location = models.ForeignKey(Location, models.CASCADE, verbose_name = "Локация")
    car = models.ForeignKey("car.Car", models.CASCADE, verbose_name = "Машина")
    blocked = models.BooleanField(default=False, verbose_name = "Блокирован")

    history = HistoricalRecords()

    class Meta:
        unique_together = (("car", "location"),)
    
    def __str__(self) -> str:
        return f"{self.car} ({self.car.user})"


def invite_expires_at():
    current_time = aware_utcnow()
    return current_time + InviteUUID.lifetime


class InviteUUID(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    location = models.ForeignKey(Location, models.CASCADE, verbose_name = "Локация")
    expires_at = models.DateTimeField(default=invite_expires_at, verbose_name = "Истекает")
    lifetime = datetime.timedelta(days=1)

    class Meta:
        verbose_name = "Инвайт"
        verbose_name_plural = "Инвайти"

    @property
    def url(self):
        return f"{INVITE_URL}/{self.uuid}/"
    
    def validate(self):
        current_time = aware_utcnow()
        if self.expires_at <= current_time - self.lifetime:
            raise exceptions.ValidationError(_("UUID has expired"), "uuid_expired")
        return self
    
    def accept_invite(self, user: User) -> UserInLocation:
        if UserInLocation.objects.filter(user=user, location=self.location).exists():
            raise exceptions.ValidationError(_("This user already in location"), "user_already_in_location")
        uil = UserInLocation.objects.create(
            user=user, location=self.location
        )
        self.delete()
        return uil


class CameraInLocation(models.Model):
    name = models.CharField(max_length=255, verbose_name = "Название")
    camera = models.OneToOneField("camera.Camera", models.CASCADE, verbose_name = "Камера")
    location = models.ForeignKey("location.Location", models.CASCADE, verbose_name = "Локация")
    mode = models.CharField(max_length=255, choices=MODES, null=True, blank=True, verbose_name = "Собития")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Камера в локации"
        verbose_name_plural = "Камеры в локации"

    def __str__(self) -> str:
        return f"{self.name} ({self.camera}:{self.location})"


class History(models.Model):
    cil = models.ForeignKey(CameraInLocation, models.CASCADE, verbose_name = "Камера в локации")
    date = models.DateTimeField(auto_now_add=True, verbose_name = "Дата")
    car = models.ForeignKey("car.Car", models.SET_NULL, blank=True, null=True, verbose_name = "Машина")
    car_number = models.CharField(max_length=255, verbose_name = "Номер машини")
    car_user = models.ForeignKey(User, models.CASCADE, verbose_name = "Пользователь")
    mode = models.CharField(default=MODE_IN, choices=MODES, max_length=255, verbose_name = "Собития")

    class Meta:
        verbose_name = "История локации"
        verbose_name_plural = "Истории локации"