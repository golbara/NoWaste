
from django.shortcuts import get_object_or_404,render, redirect
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
        email = request.data.get('email')
        password = request.data.get('password')
        user = Customer.objects.get(email = email,password = password)
        if not user:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
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

