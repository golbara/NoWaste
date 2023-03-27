
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
from rest_framework import viewsets
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from django.core.validators import EmailValidator
from django.forms import ValidationError
import random , string


# class SignUpView(APIView):

#     def post(self, request):
#         serializer = CreateUserSerializer(data=request.data)
#         if serializer.is_valid():
#             vc_code = random.randrange(100000, 999999)
#             user_data = serializer.data
#             template = render_to_string('email_template.html',
#                         {'name': user_data['first_name'] + " " + user_data['last_name'],
#                             'code': vc_code})
#             data = {'to_email':user_data['email'],'body':template, 'subject': 'Welcome to NoWaste!(Verify your email)'}
#             Util.send_email(data)
#             if (VerifyEmail()):
#                 serializer.save()
#                 user = Customer.objects.get(email = user_data['email'])
#                 token = RefreshToken.for_user(user).access_token
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             # AFTER EMAIL VERIFIACITON , THE TOKEN SET for the user 
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def get(self,request):
#         serializer = CreateUserSerializer()
#         return Response(serializer.data)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        pass
    def post(self, request):
        data = request.data
        return True
        # if(data['vc_code'] == vc_code):
            #mitoone vc_code baraye har user be model ezafe beshe.
            # pass

class SignUpView(APIView):

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            #if(# email verification):
            serializer.save()
            user_data = serializer.data
            user = Customer.objects.get(email = user_data['email'])

            token = RefreshToken.for_user(user).access_token
            vc_code = random.randrange(100000, 999999)
            template = render_to_string('email_template.html',
                                    {'name': user.first_name + " " + user.last_name,
                                     'code': vc_code})
            data = {'to_email':user.email,'body':template, 'subject': 'Welcome to NoWaste!(Verify your email)'}
            Util.send_email(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # AFTER EMAIL VERIFIACITON , THE TOKEN SET for the user 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        serializer = CreateUserSerializer()
        return Response(serializer.data)
    # def verifyEmail(self, request, currect_vc):
    #     # if 


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


class ForgotPasswordViewSet(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer()
        validate_email = EmailValidator()
        email = request.data.get('email')
        try:
            validate_email.__call__(email)
        except ValidationError as e:
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return Response("There is not any user with the given email" , status=status.HTTP_404_NOT_FOUND)
        newPassword = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        user.password = newPassword
        user.save()
        template = render_to_string('forgotpass_template.html',
            {'name': str(user.first_name) + " " + str(user.last_name),
                'code': newPassword})
        data = {'to_email':user.email,'body':template, 'subject': 'NoWaste forgot password'}
        Util.send_email(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get(self, request):
        serializer = ForgotPasswordSerializer()
        return Response(serializer.data)