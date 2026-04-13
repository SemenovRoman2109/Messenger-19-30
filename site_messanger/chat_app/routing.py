from django.urls import path
from .consumers import *

websockets_urlpatterns = [
    path('chat', ChatConsumer.as_asgi())
]