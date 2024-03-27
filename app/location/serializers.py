from drf_spectacular.utils import extend_schema_field, extend_schema_serializer
from rest_framework import serializers
from oauth.serializers import AccountSerializer
from car.serializers import CarSerializer
from camera.serializers import CameraSerializer
from .models import Location, UserInLocation, CarInLocation, CameraInLocation, INVITE_STATUS_ACCEPTED


class LocationSerializer(serializers.ModelSerializer):
    count_cars = serializers.SerializerMethodField
    accepted_count_users = serializers.SerializerMethodField()
    checking_count_users = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = "__all__"

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
    user = AccountSerializer()

    class Meta:
        model = UserInLocation
        exclude = ["location"]
        
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

    def update(self, instance, validated_data):
        validated_data["status"] = INVITE_STATUS_ACCEPTED
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
    

class CameraInLocationSerializer(serializers.ModelSerializer):
    camera = CameraSerializer()

    class Meta:
        model = CameraInLocation
        exclude = ["location"]



class CameraInLocationPatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = CameraInLocation
        exclude = ["camera", "location"]
    