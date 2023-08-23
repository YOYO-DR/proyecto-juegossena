"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
from apps.chat.routing import websocket_urlpatterns


settings_module = 'config.production' if 'WEBSITE_HOSTNAME' in os.environ else 'config.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = ProtocolTypeRouter({
    # si esta desplegado o no, pongo el protocolo
    "https" if 'WEBSITE_HOSTNAME' in os.environ else "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})