# chat/urls.py
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views
from .views import *


# urlpatterns = [
#     path("", views.index, name="index"),
#     #  path("chat_room/", views.room, name="room"),
#     path("<str:room_name>/", views.room, name="room"),
# ]

app_name = 'chat'

router = routers.DefaultRouter()
# router.register('', ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
    # path('room/<str:room_name>/user_id/<int:user_id>', views.room, name='room')
]