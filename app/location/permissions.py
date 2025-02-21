from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _
from .models import UserInLocation, INVITE_STATUS_ACCEPTED, ROLE_ADMIN, CameraInLocation


class AdminPermission(BasePermission):
    message = _('Has not admin permission')

    def has_permission(self, request, view):
        qs = UserInLocation.objects.filter(
            user=request.user,
            status=INVITE_STATUS_ACCEPTED, role=ROLE_ADMIN)
        if view.kwargs.get('location_id'):
            qs = qs.filter(location_id=view.kwargs.get('location_id'))
        if view.kwargs.get('cil_id'):
            cil = CameraInLocation.objects.get(id=view.kwargs.get('cil_id'))
            qs = qs.filter(location_id=cil.location_id)
        return qs.exists()

    def has_object_permission(self, request, view, obj):
        location = obj.location if hasattr(obj, 'location') else obj
        return UserInLocation.objects.filter(
            user=request.user, location=location,
            status=INVITE_STATUS_ACCEPTED, role=ROLE_ADMIN).exists()