from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import RegisterHistorySerializer

class RegisterView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterHistorySerializer


class CameraOpenView(CreateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        # send_data_camera(instance.id, {})
        return Response({"message": "Request sended"})
