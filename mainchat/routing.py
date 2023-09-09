from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from .consumers import ChatConsumer  # Import your WebSocket consumer

application = ProtocolTypeRouter({
    # Use the URLRouter to route WebSocket requests
    'websocket': URLRouter(
        re_path('ws/chat_msg_path/', ChatConsumer.as_asgi()),  # Replace 'some_path' with your desired path
    ),
}) 