from rest_framework.generics import CreateAPIView
from .serializers import RegisterHistorySerializer


class RegisterView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterHistorySerializer
