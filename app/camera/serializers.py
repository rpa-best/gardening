from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from location.models import History, CameraInLocation, CarInLocation
from .models import Camera


class CameraSerializer(serializers.ModelSerializer):

    class Meta:
        model = Camera
        exclude = ["id"]


class RegisterHistorySerializer(serializers.ModelSerializer):
    camera = serializers.PrimaryKeyRelatedField(queryset=Camera.objects, write_only=True)
    number = serializers.CharField()
    message = serializers.CharField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    code = serializers.CharField(read_only=True)

    class Meta:
        model = History
        fields = ["camera", "number", "message", "date", "code"]

    def register_error(self, message, code):
        raise ValidationError({"message": message, "code": code})

    def validate(self, attrs):
        camera: Camera = attrs["camera"]
        number: str = attrs["number"]
        number = number.strip().replace(" ", "")
        cil = CameraInLocation.objects.filter(camera=camera).first()
        if not cil:
            self.register_error("Camera not added to location", "camera_not_added_to_location")
        
        try:
            car = CarInLocation.objects.get(location=cil.location, car__number=number)
        except CarInLocation.DoesNotExist:
            return self.register_error("Car not added to location", "car_not_added_to_location")
        
        if car.blocked:
            self.register_error("Car is blocked", "car_blocked")
        
        validated_data = {
            "cil": cil,
            "car_number": number,
            "car": car.car,
            "car_user": car.car.user,
            "mode": cil.mode        
        }
        return super().validate(validated_data)
    
    def create(self, validated_data):
        instance: History = super().create(validated_data)
        instance.send_ws_data()
        return {
            "number": instance.car_number,
            "message": "History successfuly added",
            "date": instance.date,
            "code": "history_added_success"
        }
    