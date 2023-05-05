from django.db import models
from NoWaste.settings import *
# Create your models here.
class ChatRoom(models.Model):
    title = models.CharField(max_length=255,unique=True,blank=False)
    user1 = models.ForeignKey(AUTH_USER_MODEL,on_delete= models.CASCADE,related_name = 'user1')
    user2 = models.ForeignKey(AUTH_USER_MODEL,on_delete= models.CASCADE,related_name = "user2")

 
    def __str__(self):
        return self.title
    
    def connect_user(self,user):
        " return true if user is added to the users list."
        is_user_added = False
        if not user in self.users.all:
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added
    

    def disconnect_user(self,user):
        " return true if user is added to the users list."
        is_user_removed = False
        if  user in self.users.all:
            self.users.remove(user)
            self.save()
            is_user_removed= True
        return is_user_removed
    
    @property
    def group_name(self):
        return f"ChatRoom-{self.id}"
    
class Message(models.Model):
    user  = models.ForeignKey(AUTH_USER_MODEL,on_delete= models.CASCADE)
    room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    timestamp  = models.DateTimeField(auto_now_add=True)
    content  = models.TextField(unique= False,blank=False)

    def __str__(self) :
        return self.content
    
    def last_30_messages(self):
        return Message.objects.order_by('-timestamp').all()[:30]
