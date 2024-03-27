from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin
from django_celery_beat.models import SolarSchedule, ClockedSchedule, IntervalSchedule
from django_celery_results.models import GroupResult
from car.models import Car
from .models import User

admin.site.name = "Садоводство"
admin.site.site_header = "Садоводство"
admin.site.unregister([SolarSchedule, ClockedSchedule, IntervalSchedule, GroupResult])


class CarInline(admin.TabularInline):
    model = Car
    extra = 0


@admin.register(User)
class UserAdmin(SimpleHistoryAdmin, _UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "surname", "phone", "max_cars_count")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "surname", "is_staff")
    ordering = ("email",)
    search_fields = User.autocomplete_search_fields()
    readonly_fields = ["date_joined", "last_login"]
    inlines = [CarInline]
