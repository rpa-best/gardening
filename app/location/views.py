from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Location, UserInLocation, CarInLocation, INVITE_STATUS_ACCEPTED, INVITE_STATUS_CHECKING, ROLE_ADMIN
from .permissions import AdminPermission
from .serializers import (
    LocationSerializer, UserInLocationListSerializer, 
    UserInLocationPatchSerializer, UserInLocationAcceptSerializer,
    CarInLocationSerializer, CarInLocationPostSerializer
)

class LocationView(ReadOnlyModelViewSet):
    serializer_class = LocationSerializer
    
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Location.objects.all()
        return Location.objects.filter(userinlocation__user=self.request.user)


class UserInLocationView(ModelViewSet):
    http_method_names = ["get", "head", "patch", "delete"]
    permission_classes = (IsAuthenticated, AdminPermission)

    def get_serializer_class(self):
        if self.action in ["list", 'retrieve']:
            return UserInLocationListSerializer
        return UserInLocationPatchSerializer
    
    def get_queryset(self):
        return UserInLocation.objects.filter(location_id=self.kwargs.get("location_id"), status=INVITE_STATUS_ACCEPTED)
    
    def perform_destroy(self, instance:UserInLocation):
        if instance.user.id == self.request.user.id:
            raise ValidationError("This user is you", "user_not_deletable")
        if instance.role == ROLE_ADMIN:
            raise ValidationError("This user also admin, you dont delete this user", "user_not_deletable")
        return super().perform_destroy(instance)


class UserInLocationInviteView(ModelViewSet):
    http_method_names = ["get", "head", "patch", "delete"]
    permission_classes = (IsAuthenticated, AdminPermission)

    def get_serializer_class(self):
        if self.action in ["list", 'retrieve']:
            return UserInLocationListSerializer
        return UserInLocationAcceptSerializer
    
    def get_queryset(self):
        return UserInLocation.objects.filter(location_id=self.kwargs.get("location_id"), status=INVITE_STATUS_CHECKING)


class CarInLocationView(ModelViewSet):
    http_method_names = ["get", "head", "patch", "post", "delete"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CarInLocationSerializer
        if self.action == "partial_update":
            return None
        return CarInLocationPostSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return CarInLocation.objects.all()
        if UserInLocation.objects.filter(user=self.request.user, location_id=self.kwargs.get("location"), role=ROLE_ADMIN, status=INVITE_STATUS_ACCEPTED):
            return CarInLocation.objects.filter(location_id=self.kwargs.get("location_id"))
        return CarInLocation.objects.filter(location_id=self.kwargs.get('location_id'), car__user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        request.data.update(location=self.kwargs.get("location_id"))
        return super().create(request, *args, **kwargs)
    
    def perform_destroy(self, instance: CarInLocation):
        if instance.car.user.id == self.request.user.id:
            return super().perform_destroy(instance)
        instance.blocked = True
        instance.save()

    def update(self, request, *args, **kwargs):
        instance: CarInLocation = self.get_object()
        if instance.car.user == self.request.user:
            raise ValidationError("You not activate own car", "not_activate_own_car")
        instance.blocked = False
        instance.save()
        return Response(CarInLocationSerializer(instance, context=self.get_serializer_context()).data)


class UserInLocationCarView(CarInLocationView):
    http_method_names = ["get", "head", "patch", "delete"]

    def get_queryset(self):
        return CarInLocation.objects.filter(location_id=self.kwargs.get("location_id"), car__user_id=self.kwargs.get("user_id"))
