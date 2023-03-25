
from django.shortcuts import get_object_or_404,render, redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, permission_classes
from .serializers import *
from .models import *
from .utils import Util
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpView(APIView):

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            #if(# email verification):
            serializer.save()
            user_data = serializer.data
            user = Customer.objects.get(email = user_data['email'])

            token = RefreshToken.for_user(user).access_token
            
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://' + current_site + relativeLink + "?token="+str(token)
            data = {'to_email':user.email,'domain':absurl, 'subject': 'Verify your email'}
            # print(user.email)
            Util.send_email(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # AFTER EMAIL VERIFIACITON , THE TOKEN SET for the user 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        serializer = CreateUserSerializer()
        return Response(serializer.data)

class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass
    


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = get_object_or_404(Customer, email = email , password = password)
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


    
class CustomerViewSet(ModelViewSet,UpdateModelMixin):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class =CustomerSerializer
    queryset = Customer.objects.all()

    def create(self, request):
        queryset = Customer.objects.all()
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Customer.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CustomerSerializer(user)
        return Response(serializer.data)
    def update(self, request, pk=None):
        super().update(request,pk = pk)

    def partial_update(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        super().destroy(request= request ,pk = pk)
