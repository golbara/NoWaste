from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import  login_required
import json
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import ChatSerializer
from .models import *
from User.models import *
# def index(request):
#     return render(request, "chat/index.html")
# # # @login_required
# # def room(request, room_name):
# #     return render(request, "chat/room.html", {"room_name": mark_safe(json.dumps(room_name))})

# def room(request, room_name):
#     room = ChatRoom.objects.get_or_create(title = room_name)
#     # messages  = Message.objects.filter(room = room)[0:25]
#     print(room)
#     print(mark_safe(json.dumps(request.user.id)))
#     # messages = Message.objects.filter(room = room.id)[0:25]
#     # return render(request, "chat/room.html", {"room_name": room_name})
#     # return render(request, "chat/room.html", {"room_name": room_name,"messages": messages ,"user_name":mark_safe(json.dumps(request.user.email))})
#     # return render(request, "chat/room.html", {"room_name": room_name,"user_name":mark_safe(json.dumps(request.user.email))})
#     return render(request, "chat/room.html", {"room_name": room_name,"user_id":mark_safe(json.dumps(request.user.id))})



# # "user_name":mark_safe(json.dumps(request.user.email))}

# # def fetch(request,room_name):
# #     return Response(Message.objects.filter(user = request.user ,))
# # ,"user_name":mark_safe(json.dumps(request.user.email))

class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    # permission_classes = IsAuthenticated
    @action(
        detail=False,
        methods=['get', 'post'],
        url_path=r'index',
        url_name='chat_index',
        permission_classes=[AllowAny]
    )
    def index(self, request):
        return render(request, 'chat/index.html')
    
    @action(
        detail=True,
        methods=['get', 'post'],
        url_path=r'room/(?P<room_name>\w+)/user_id/(?P<user_id>\w+)',
        url_name='chat_room',
        permission_classes=[AllowAny]
    )
    def room(self, request, room_name, user_id):
        messages = Chat.objects.filter(room=room_name)
        print("messssssages22222:")
        print (messages)
        return render(request, 'chat/room.html', {'room_name': room_name, 'user_id': user_id, 'messages': messages})
    
    @action(
        detail=False,
        methods=['get', 'post'],
        url_path=r'room/messages/(?P<room_name>\w+)',
        url_name='chat_room',
        permission_classes=[AllowAny]
    )
    def get_room_messages(self, request, room_name, *args, **kwargs):
        
        try:
            chats = Chat.objects.filter(room_name=room_name)
            serializer = ChatSerializer(chats, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        
    def room(request, room_name, user_id):
        messages = Chat.objects.filter(room_name=room_name)
        user = Customer.objects.get(id=user_id)
        return render(request, 'chat/room.html', {'room_name': room_name, 'user_id': user_id, 'messages': messages, 'username': user.username})