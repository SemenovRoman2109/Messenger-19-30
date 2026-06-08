"""
ASGI config for site_messanger project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat_app.routing import websockets_urlpatterns
from user_app.routing import user_websockets_urlpatterns
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_messanger.settings')


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(websockets_urlpatterns + user_websockets_urlpatterns))
})

# @database_sync_to_async - декоратор що допомагає перетворити синхронну функцію в асинхронну (тому-що робота з БД - синхронна) з channels.db 
# Щоб в consumers отримати акаунт користувача self.scope.get("user"), також в asgi за ключем 'websocket': AuthMiddlewareStack(URLRouter(...))