# from django.urls import re_path

# # from . import consumers
# # "build asgi application for our web socket"
# # websocket_urlpatterns = [
# #     re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
# # ]

# from chat.consumers import ChatConsumer

# websocket_urlpatterns = [
#     re_path(r'ws://chat/room/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
#     # re_path(r'ws/chat/room/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
# ]


# from django.urls import re_path

# from channels.routing import ProtocolTypeRouter, URLRouter
# from chat.consumers import ChatConsumer

# websocket_urlpatterns = [
#     re_path(r'ws/chat/room/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
# ]

# application = ProtocolTypeRouter({
#     'websocket': URLRouter(websocket_urlpatterns),
# })
# from django.urls import re_path

# from chat.consumers import ChatConsumer

# websocket_urlpatterns = [
#     re_path(r'room/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
# ]

# from django.urls import re_path 
 
# # from . import consumers 
# # "build asgi application for our web socket" 
# # websocket_urlpatterns = [ 
# #     re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()), 
# # ] 
 
# from chat.consumers import ChatConsumer 
 
# websocket_urlpatterns = [ 
#     re_path(r'room/(?P<room_name>\w+)/$<int:user_id>/', ChatConsumer.as_asgi()), 
#     # re_path(r'ws/chat/room/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()), 
# ]


from django.urls import re_path 
 
from chat.consumers import ChatConsumer 
 
websocket_urlpatterns = [
    re_path(r'chat/room/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]