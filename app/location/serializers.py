from drf_spectacular.utils import extend_schema_field, extend_schema_serializer
from rest_framework import serializers
from oauth.serializers import UserShortSerializer
from car.serializers import CarSerializer
from camera.serializers import CameraSerializer
from .models import Location, UserInLocation, CarInLocation, CameraInLocation, InviteUUID, History, INVITE_STATUS_ACCEPTED


class CameraInLocationSerializer(serializers.ModelSerializer):
    camera = CameraSerializer()

    class Meta:
        model = CameraInLocation
        exclude = ["location"]


class LocationSerializer(serializers.ModelSerializer):
    count_cars = serializers.SerializerMethodField()
    accepted_count_users = serializers.SerializerMethodField()
    checking_count_users = serializers.SerializerMethodField()
    cameras = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = "__all__"

    @extend_schema_field(serializers.CharField())
    def get_status(self, obj: Location):
        return obj.userinlocation_set.get(user=self.context["request"].user).status

    @extend_schema_field(serializers.CharField())
    def get_role(self, obj: Location):
        return obj.userinlocation_set.get(user=self.context["request"].user).role

    @extend_schema_field(CameraInLocationSerializer(many=True))
    def get_cameras(self, obj: Location):
        return CameraInLocationSerializer(obj.camerainlocation_set.all(), many=True, context=self.context).data

    @extend_schema_field(serializers.IntegerField())
    def get_count_cars(self, obj: Location):
        return obj.count_cars

    @extend_schema_field(serializers.IntegerField())
    def get_accepted_count_users(self, obj: Location):
        return obj.accepted_count_users

    @extend_schema_field(serializers.IntegerField())
    def get_checking_count_users(self, obj: Location):
        return obj.checking_count_users


class UserInLocationListSerializer(serializers.ModelSerializer):
    count_cars = serializers.SerializerMethodField()
    user = UserShortSerializer()
    location = LocationSerializer()

    class Meta:
        model = UserInLocation
        fields = "__all__"

    @extend_schema_field(serializers.IntegerField())
    def get_count_cars(self, obj: UserInLocation):
        return obj.count_cars


class UserInLocationPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInLocation
        fields = ["max_count_cars"]


class UserInLocationAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInLocation
        fields = ["max_count_cars"]

    def update(self, instance: UserInLocation, validated_data):
        instance.accept(**validated_data)
        return super().update(instance, validated_data)


class CarInLocationSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = CarInLocation
        exclude = ["location"]


@extend_schema_serializer(exclude_fields=["location"])
class CarInLocationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarInLocation
        fields = "__all__"

    def create(self, validated_data):
        location: Location = validated_data["location"]
        car = validated_data["car"]
        return location.add_car(car)


class CameraInLocationPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraInLocation
        exclude = ["camera", "location"]


class InviteShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = InviteUUID
        fields = ["expires_at", "uuid"]


class HistorySerializer(serializers.ModelSerializer):
    cil = CameraInLocationSerializer()
    car = CarSerializer()
    car_user = UserShortSerializer()

    class Meta:
        model = History
        fields = "__all__"