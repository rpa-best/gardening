from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from .models import Car


@extend_schema_serializer(exclude_fields=["user"])
class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = "__all__"
    
    def create(self, validated_data):
        return Car.add_car(**validated_data)
