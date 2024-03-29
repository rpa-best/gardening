from django.urls import path

from oauth.consumers import NotificationConsumer
from camera.consumers import CameraConsumer


websocket_urlpatterns = [
    path('ws/api/notification/', NotificationConsumer.as_asgi()),
    path('ws/api/camera/', CameraConsumer.as_asgi()),
]
