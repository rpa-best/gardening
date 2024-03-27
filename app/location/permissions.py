from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _
from .models import UserInLocation, INVITE_STATUS_ACCEPTED, ROLE_ADMIN


class AdminPermission(BasePermission):
    message = _('Has not admin permission')

    def has_permission(self, request, view):
        locaton_id = view.kwargs.get("location_id")
        return UserInLocation.objects.filter(
            user=request.user, location_id=locaton_id, 
            status=INVITE_STATUS_ACCEPTED, role=ROLE_ADMIN).exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)