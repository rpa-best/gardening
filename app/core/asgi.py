"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'py_keyman24_ru.settings')
django.setup()

from core.routing import websocket_urlpatterns
from core.utils.middlewares import WebsocketMiddlewareStack

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": WebsocketMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})