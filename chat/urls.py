# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    #  path("chat_room/", views.room, name="room"),
    path("<str:room_name>/", views.room, name="room"),
]