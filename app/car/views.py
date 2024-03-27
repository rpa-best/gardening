from rest_framework.viewsets import ModelViewSet
from .models import Car
from .serializers import CarSerializer


class CarView(ModelViewSet):
    http_method_names = ["get", "head", "post", "patch", "delete"]
    serializer_class = CarSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Car.objects.all()
        return Car.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        request.data.update(user=request.user.id)
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        request.data.update(user=request.user.id)
        return super().update(request, *args, **kwargs)
    