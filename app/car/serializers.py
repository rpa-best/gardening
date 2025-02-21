from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from oauth.serializers import UserShortSerializer
from .models import Car


@extend_schema_serializer()
class CarSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    locations = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Car
        fields = "__all__"
    
    def create(self, validated_data):
        locations = validated_data.pop("locations", None)
        car = Car.add_car(**validated_data, user=self.context['request'].user)
        car.add_location(locations) if locations is not None else None
        return car

    def update(self, instance, validated_data):
        instance.add_location(validated_data.pop('locations')) if not validated_data.get('locations') is None else None
        return super(CarSerializer, self).update(instance, validated_data)
