from django.contrib import admin
from django.core.paginator import *
from django.core.cache import cache
from django.db import models
from .models import *

# Register your models here.
# class ChatRoomAdmin(admin.ModelAdmin):
#     list_display = ['id','title']
#     search_fields = ['id','title']
#     list_display = ['id',]

#     class Meta : 
#         model = ChatRoom

# admin.site.register(ChatRoom,ChatRoomAdmin)


# class CachingPaginatoin(Paginator):
#     def _get_count(self):
#         if not hasattr(self,"_count"):
#             self._count = None
#         if self._count is None:
#             try:
#                 key = "adm: {0} : count".format(hash(self.object_list.query.__str__()))
#                 self._count = cache.get(key, -1)
#                 if self._count == -1:
#                     self._count = super().count
#                     cache.set(key,self._count,3600)
#             except:
#                 self._count = len(self.object_list)
#         return self._count
    
#     count = property(_get_count)

# class MessageAdmin(admin.ModelAdmin):
#     list_filter = ['room','user','timestamp']
#     list_display = ['room','user','timestamp','content']
#     search_fields= ['room__title','user__username','content']
#     readonly_fields = ['id','user','room','timestamp']

#     show_full_result_count = False
#     paginator = CachingPaginatoin
#     class Meta :
#         model = Message

# admin.site.register(Message,MessageAdmin)

class ChatAdmin(admin.ModelAdmin):
    ordering = ['date_created']
    list_display = ['room_name', 'sender', 'date_created']
    list_filter = ['sender','room_name']
    search_fields = ('room_name',)
# admin.site.register(Chat, ChatAdmin)