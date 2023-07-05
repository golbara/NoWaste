from django.db import models
from django.conf import settings
from User.models import *

class Chat(models.Model):

    sender = models.ForeignKey(MyAuthor, related_name='chats_sender', on_delete=models.CASCADE)
    reciever = models.ForeignKey(MyAuthor, related_name='chats_reciever', on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=250)
