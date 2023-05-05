from django.urls import re_path

from . import consumers
"build asgi application for our web socket"
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]