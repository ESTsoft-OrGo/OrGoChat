from django.urls import path, re_path
from .consumers import ChatConsumer, GroupChatConsumer

websocket_urlpatterns = [
    path('chat/<str:room_name>', ChatConsumer.as_asgi()),
    path('groupchat/<str:room_name>', GroupChatConsumer.as_asgi()),
]