"""
ASGI config for aufguss_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from aufguss_app import routing as aufguss_routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aufguss_backend.settings")
django.setup()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(aufguss_routing.websocket_urlpatterns)
        ),
    }
)
