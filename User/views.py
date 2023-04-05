
from django.contrib.auth import get_user_model,logout
from rest_framework.permissions import BasePermission
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render, redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import *
from .utils import Util
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework.authentication import TokenAuthentication
###############################################
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_jwt.settings import api_settings

from rest_framework import generics
from django.template.loader import render_to_string
from django.core.validators import EmailValidator
from django.forms import ValidationError
import random , string
import jwt


class VerifyEmail(generics.GenericAPIView):
    serializer_class =EmailVerificationSerializer
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.data
            try:
                user = Customer.objects.get(email = user_data['email'])
            except Customer.DoesNotExist:
                return Response("There is not any user with the given email" , status=status.HTTP_404_NOT_FOUND)
            if user.vc_code == user_data['code']:
                user.email_confirmed = True
                user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'code is wrong'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        serializer = EmailVerificationSerializer()
        return Response(serializer.data)


# class SignUpView(APIView):

#     def post(self, request):
#         serializer = CreateUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # email = request.data.get('email')
#             # role = request.data.get('role')
#             #if(# email verification):
#             # user = serializer.save()
#             user_data = serializer.data
#             if (user_data['role'] == "customer"):
#             # if (role == "customer"):
#                 try :
#                     # user = Customer.objects.get(email = email)
#                     user = Customer.objects.get(email = user_data['email'])
#                     return Response( "customer with this email already exists.",status= status.HTTP_400_BAD_REQUEST)
#                     # return Response("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii",status= status.HTTP_100_CONTINUE)
#                 except :
#                     # serializer.save(user = request.data)
#                     # print("3")
#                     # print("4")
#                     user.email_confirmed = False
#                     user.vc_code = vc_code
#                     user.set_password(user_data['password'])
#                     user.save()
#             user_data = serializer.data
#             print("1")
#             print(user_data)
#             print("2")
#             user = None
#             # token = RefreshToken.for_user(user).access_token
#             vc_code = random.randrange(100000, 999999)
#             template = render_to_string('email_template.html',
#                                     {'name': user.name,
#                                      'code': vc_code})
#             data = {'to_email':user.email,'body':template, 'subject': 'Welcome to NoWaste!(Verify your email)'}
#             Util.send_email(data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#             # AFTER EMAIL VERIFIACITON , THE TOKEN SET for the user 
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def get(self,request):
#         serializer = CreateUserSerializer()
#         return Response(serializer.data)

class SignUpView(APIView):

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            #if(# email verification):
            serializer.save()
            user_data = serializer.data
            # token = RefreshToken.for_user(user).access_token
            vc_code = random.randrange(100000, 999999)
            if (user_data['role'] == "customer"):
                user = Customer.objects.get(email = user_data['email'])
                user.email_confirmed = False
                user.vc_code = vc_code
                user.save()
            template = render_to_string('email_template.html',
                                    {'name': user.name,
                                     'code': vc_code})
            data = {'to_email':user.email,'body':template, 'subject': 'Welcome to NoWaste!(Verify your email)'}
            Util.send_email(data)
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
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.check_password(password):
        # if user.password == password:
            token, _ = Token.objects.get_or_create(user=user)
            # token = obtain_auth_token
            return Response({'token': token.key})
            # if user.email_confirmed:
            #     token, _ = Token.objects.get_or_create(user=user)
            #     return Response({'token': token.key})
            # else:
            #     return Response({'error': 'email not confirmed'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    def get(self,request):
        serializer = LoginSerializer()
        return Response(serializer.data)
    
# def get_auth_headers(token):
#     return {'Authorization': f'Token {token}'}

# @permission_classes((IsAuthenticated,))
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Get the token from the user's request
        token = request.auth
        
        # Create a response with headers
        response = HttpResponse(content_type='application/json')
        response['Authorization'] = f'Token {token}'
        
        # Return the response
        return response
    def Post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        logout(request)
        return Response({'message': 'User logged out successfully'})

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
        user.set_password(newPassword)
        user.save()
        template = render_to_string('forgotpass_template.html',
            {'name': user.name,
                'code': newPassword})
        data = {'to_email':user.email,'body':template, 'subject': 'NoWaste forgot password'}
        Util.send_email(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get(self, request):
        serializer = ForgotPasswordSerializer()
        return Response(serializer.data)
    
class AllowAnyUser(BasePermission):
    def has_permission(self, request, view):
        return True

class ChangePasswordView(generics.UpdateAPIView):
    queryset = Customer.objects.all()
    # authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    # permission_classes = [AllowAnyUser]
    serializer_class = ChangePasswordSerializer
    def put(self, request, *args, **kwargs):
        # return super().partial_update(request, *args, **kwargs)
        print(request.auth)
        return super().update(request, *args, **kwargs) 

class UpdateProfileView(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    serializer_class = UpdateUserSerializer

    def partial_update(self, request, *args, **kwargs):
        # Implement partial_update logic here
        return super().partial_update(request, *args, **kwargs)
    # def get_serializer_context(self):
    #     return {'customer_id': self.kwargs['customer_pk']}

    # def get_queryset(self):
    #     return Customer.objects \
    #         .filter(pk=self.kwargs['id']) 
            # .select_related('product')
# class UpdateProfileView(generics.UpdateAPIView):
#     queryset = Customer.objects.all()
#     # permission_classes = (IsAuthenticated,)
#     lookup_field = 'id'
#     serializer_class = UpdateUserSerializer
#     def put(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)
#     def get(self,request):
#         serializer = UpdateUserSerializer()
#         return Response(serializer.data)

from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Customer
from .serializers import UpdateUserSerializer

class UpdateProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        customer, _ = Customer.objects.get_or_create(user=user)
        serializer = self.get_serializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
