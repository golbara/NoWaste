from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import  login_required
import json
from .models import *
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