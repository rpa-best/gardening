from typing import Any
from django.contrib.gis import admin
from django.db.models.query import QuerySet
from django.utils.html import format_html
from .models import Location, UserInLocation, CarInLocation, InviteUUID, INVITE_STATUS_CHECKING, INVITE_STATUS_ACCEPTED


class UserInLocationInline(admin.TabularInline):
    model = UserInLocation
    extra = 0
    verbose_name = "Ползователь"
    verbose_name_plural = "Ползователи"
    
    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def get_queryset(self, request) -> QuerySet[Any]:
        return super().get_queryset(request).filter(status=INVITE_STATUS_ACCEPTED)



class UserInLocationInviteInline(admin.TabularInline):
    model = UserInLocation
    extra = 0
    verbose_name = "Заявка"
    verbose_name_plural = "Заявки"

    def get_queryset(self, request) -> QuerySet[Any]:
        return super().get_queryset(request).filter(status=INVITE_STATUS_CHECKING)


class CarInLocationInline(admin.TabularInline):
    model = CarInLocation
    extra = 0
    readonly_fields = ["user"]
    fields = ["user", "car"]

    @admin.display(description="User")
    def user(self, obj: CarInLocation):
        return str(obj.car.user)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "users", "cars"]
    inlines = [UserInLocationInline, UserInLocationInviteInline, CarInLocationInline]

    @admin.display(description="Users")
    def users(self, obj: Location):
        return f"{obj.checking_count_users}/{obj.accepted_count_users}/{obj.max_count_users}"
    
    @admin.display(description="Cars")
    def cars(self, obj: Location):
        return f"{obj.count_cars}/{obj.max_count_cars}"


@admin.register(UserInLocation)
class UserInLocationAdmin(admin.ModelAdmin):
    list_display = ["user", "location", "status", "max_count_cars"]
    list_filter = ["user", "location", "status"]
    actions = ["accept_invites"]

    @admin.action(description="Accept invite")
    def accept_invites(self, request, queryset):
        for uil in queryset:
            uil.accept()
    

@admin.register(InviteUUID)
class InviteUUIDAdmin(admin.ModelAdmin):
    list_display = ["uuid", "location", "expires_at"]
    readonly_fields = ["uuid", "expires_at", "get_url"]
    fields = ["uuid", "location", "expires_at", "get_url"]

    @admin.display(description="url")
    def get_url(self, obj: InviteUUID):
        if not obj:
            return "-"
        return format_html(f"<a href={obj.url}>{obj.url}</a>")

    def has_change_permission(self, request, obj=None) -> bool:
        return False
