"""
ASGI config for NoWaste project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NoWaste.settings")

django.setup()

from django.core.asgi import get_asgi_application

application = get_asgi_application()


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chat.routing import websocket_urlpatterns




# application = ProtocolTypeRouter(
#     {
#         "http": application,
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
#         ),
#     }
# )

application = ProtocolTypeRouter({
    "http": application,
     "websocket": AuthMiddlewareStack(
         URLRouter(
             websocket_urlpatterns
         )
     ),
})
