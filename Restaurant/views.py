from django.contrib.auth import get_user_model,logout
from rest_framework.permissions import BasePermission
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render, redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status ,generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import *
from .models import *
from rest_framework.authentication import TokenAuthentication

class ChangePasswordView(generics.UpdateAPIView):
    # queryset = Restaurant.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def put(self, request, *args, **kwargs):
        user = request.user
        if(user.id != self.kwargs['pk']):
            return Response({"message": "Unathorized!"},status=status.HTTP_401_UNAUTHORIZED)
        super().update(request, *args, **kwargs) 
        return Response({"message" :"Password changed successfully!"},status= status.HTTP_200_OK)


class RestaurantView(generics.RetrieveAPIView):

    def get_queryset(self):
        # print( self.request.user.id)
        # return Restaurant.objects.get(id = self.request.user.id)
        return Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'id'
 
    
class FoodViewSet(ModelViewSet):
    serializer_class = FoodSerializer
    def get_queryset(self):
        return Food.objects.filter(Restaurant_id=self.kwargs['Restaurant_pk'])

    def get_serializer_context(self):
        return {'Restaurant_id': self.kwargs['Restaurant_pk']}

  