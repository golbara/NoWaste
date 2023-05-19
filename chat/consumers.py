# chat/consumers.py
import json
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync,  sync_to_async
from channels.generic.websocket import WebsocketConsumer , AsyncWebsocketConsumer
from .models import * 
from User.models import *

# User = get_user_model()
# # class ChatConsumer(AsyncWebsocketConsumer):
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )
#         # self.channel_layer.group_add(self.room_name,self.room_group_name)
#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#          self.channel_layer.group_discard(
#             self.room_group_name, self.channel_name)

#     def fetch_messages(self,data):
#         messages = Message.last_30_messages()
#         content = {
#             'messages': self.messages_to_json(messages)
#         }
#         self.send_message(content)
    
#     def messages_to_json(self,messages):
#         result = []
#         for message in messages:
#             result.append(self.message_to_json(message))
#         return result
    
#     def message_to_json(self,message):
#         return {
#             'author': message.user.email,
#             'content': message.content,
#             'timestamp':str(message.timestamp)
#         }

#     def new_message(self,data):
#         user = data.user
#         # author_user = User.objects.filter(username = user)[0]
#         author_user = User.objects.filter(id = user.id)[0]
#         message = Message.objects.create(author = author_user,content = data['message'])
#         content = {
#             'command':'new_message',
#             'message':self.message_to_json(message)
#         }
#         return self.send_chat_message(content)

#     commands = {
#         'fetch_messages' : fetch_messages,
#         'new_message' :new_message
#     }

#     def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
#         # name = data['name']
#         # room = data['room']
#         #  self.channel_layer.group_send(
#         #     self.room_group_name,
#         #     {
#         #         'type':'chat_message',
#         #         'message':message,
#         #         # 'name':name,
#         #         # 'room' : room,
#         #     }
#         # )
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat.message", "message": message}
#         )
#         # self.send(text_data=json.dumps({"message": message}))

#     def send_chat_message(self,message):
#         # message = text_data_json["message"]

#         # Send message to room group
#         self.channel_layer.group_send(
#             self.room_group_name, {"type": "chat.message", "message": message}
#         )

#     # # Receive message from WebSocket
#     # def receive(self, text_data):
#     #     text_data_json = json.loads(text_data)
#     #     message = text_data_json["message"]

#     #     # Send message to room group
#     #     _to_sync(self.channel_layer.group_send)(
#     #         self.room_group_name, {"type": "chat.message", "message": message}
#     #     )

#     def send_message(self,message):
#         self.send(text_data= json.dumps(message))
#     # Receive message from room group
#     def chat_message(self, event):
#         message = event["message"]
#         # name = event["name"]
#         # room = event["room"]
#         print(message)

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             "message": message,
#             # "name":name,
#             # "room": room
#         }))


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from web socket
    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user_id = data['user_id']
        room = data['room_name']
        sender_type = data['sender_type']

        user = Customer.objects.get (id = user_id)
        async_to_sync(self.save_message)(user, room, message, sender_type)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'sender_type':sender_type
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        sender_type = event['sender_type']        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'sender_type':sender_type
        }))

    @sync_to_async
    def save_message(self, user, room, message, sender_type):
        Chat.objects.create(sender=user, room_name=room, message=message, sender_type=sender_type)