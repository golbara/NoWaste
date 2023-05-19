from django.db import models
from django.conf import settings
from User.models import *
# Create your models here.
# class ChatRoom(models.Model):
#     title = models.CharField(max_length=255,unique=True,blank=False)
#     user = models.ManyToManyField(settings.AUTH_USER_MODEL,blank = True, null=True, help_text= " users who are connected to the chat .")
#     def __str__(self) -> str:
#         return self.title
    
#     def connect_user(self,user):
#         " return true if user is added to the users list."
#         is_user_added = False
#         if not user in self.users.all:
#             self.users.add(user)
#             self.save()
#             is_user_added = True
#         elif user in self.users.all():
#             is_user_added = True
#         return is_user_added
    

#     def disconnect_user(self,user):
#         " return true if user is added to the users list."
#         is_user_removed = False
#         if  user in self.users.all:
#             self.users.remove(user)
#             self.save()
#             is_user_removed= True
#         return is_user_removed
    
#     @property
#     def group_name(self):
#         return f"ChatRoom-{self.id}"
    
# class Message(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete= models.CASCADE)
#     room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     content = models.TextField(unique= False,blank=False)

#     def __str__(self) :
#         return self.content
    
#     def last_30_messages(self):
#         return Message.objects.order_by('-timestamp').all()[:30]


class Chat(models.Model):
    class SenderType(models.TextChoices):
        server = 'SERVER'
        Client = 'CLIENT'
    sender = models.ForeignKey(Customer, related_name='send_chats', on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=250)
    sender_type= models.CharField(max_length=6, choices=SenderType.choices, null=True)