
from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator
from django.views.generic import View, UpdateView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, permission_classes
from .serializers import *
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login, authenticate, logout

class SignUpView(APIView):

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            #if(# email verification):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # AFTER EMAIL VERIFIACITON , THE TOKEN SET for the user 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        serializer = CreateUserSerializer()
        return Response(serializer.data)


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        # serializer = self.serializer_class(data=request.data,
        #                                    context={'request': request})
        # serializer = LoginSerializer(data=request.data)
        # serializer.is_valid()
        userName = request.data.get('userName')
        password = request.data.get('password')
                # authenticate user
        user = authenticate(userName = userName, password=password)
        # user2 = serializer.validated_data
        if not user:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    def get(self,request):
        serializer = LoginSerializer()
        return Response(serializer.data)

@permission_classes((IsAuthenticated,))
class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response("User successfully logged out.", status = status.HTTP_200_OK)

