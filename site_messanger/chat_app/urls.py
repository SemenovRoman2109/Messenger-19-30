from django.urls import path 
from .views import *

urlpatterns = [
    path('', ChatView.as_view(), name = "chat"),
    path('create/', CreateChatView.as_view(), name = "create_chat")
]