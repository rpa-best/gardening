from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from .utils import generate_opt
from .sms import send_otp

OPT_EXPIRING_LIFESPAN = timedelta(minutes=1)

class User(AbstractUser):
    username = None
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)
    phone = PhoneNumberField(unique=True)
    surname = models.CharField(_("surname"), blank=True, null=True, max_length=255)
    max_cars_count = models.IntegerField(default=1)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'phone'

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    @property
    def name(self) -> str:
        name = []
        if self.last_name:
            name.append(self.last_name)
        
        if self.first_name:
            name.append(self.first_name)
        
        if self.surname:
            name.append(self.surname)
        return str(self.phone) if not name else " ".join(name)

    @staticmethod
    def autocomplete_search_fields():
        return ["email", "first_name", "last_name", "surname"]

    @property
    def opt_exp(self):
        now = timezone.now()
        if self.opt_lia < now - OPT_EXPIRING_LIFESPAN:
            return True
        return False

    def opt_check(self, opt):
        return self.opt == opt and not self.opt_exp

    def opt_create(self, save=True):
        self.opt = generate_opt()
        self.opt_lia = timezone.now()
        if save:
            self.save()
        return self.opt

    def send_opt(self, save=True):
        self.opt_create(save)
        if not settings.DEBUG:
            return send_otp.delay(str(self.phone), str(self.opt))
        print(self.phone, self.opt)
