from django.urls import path

from oauth.consumers import NotificationConsumer
from camera.consumers import CameraConsumer
from location.consumers import CILConsumer


websocket_urlpatterns = [
    path('api/ws/notification/', NotificationConsumer.as_asgi()),
    path('api/ws/camera/', CameraConsumer.as_asgi()),
    path('api/ws/cil/<cil_id>/', CILConsumer.as_asgi()),
]
