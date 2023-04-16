
from django.contrib.auth import get_user_model,logout
from django.contrib.auth.hashers import make_password
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

class VerifyEmail(APIView):
    def get_serializer_class(self, request):
        if request.data['role'] == "customer":
            return CreateCustomerSerializer
        elif request.data['role'] == "restaurant":
            return CreateRestaurantSerializer
    
    def post(self, request):
        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            try:
                user = VC_Codes.objects.get(email=user_data['email'])
            except VC_Codes.DoesNotExist:
                return Response("There is not any user with the given email" , status=status.HTTP_404_NOT_FOUND)
            if user_data['code'] == user.vc_code:
                serializer.save()
                return Response(user_data, status=status.HTTP_201_CREATED)
        return Response("verification code is wrong", status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        serializer = BaseCreateUserSerializer()
        return Response(serializer.data)
    
class SignUpView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception= True):
            vc_code = random.randint(100000, 999999)
            instance = serializer.save()
            instance.vc_code = vc_code
            instance.save()
            signupData = serializer.data
        else:
            return Response("email is already exist", status=status.HTTP_400_BAD_REQUEST)
        email = signupData['email']
        name = signupData['name']
        template = render_to_string('email_template.html', {'name': name, 'code': vc_code})
        data = {'to_email': email, 'body': template, 'subject': 'Welcome to NoWaste!(Verify your email)'}
        Util.send_email(data)
        return Response(signupData, status=status.HTTP_201_CREATED)
    def get(self,request):
        serializer = SignUpSerializer()
        return Response(serializer.data)
    
class LoginView(APIView):
    serializer_class = MyAuthorSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user_model = get_user_model()
        try:
            myauthor_qs = MyAuthor.objects.filter(email=email)
            if len(myauthor_qs) != 0:
                user = myauthor_qs.first()
        except user_model.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    def get(self,request):
        serializer = MyAuthorSerializer()
        return Response(serializer.data)


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
            user = MyAuthor.objects.get(email=email)
        except MyAuthor.DoesNotExist:
            return Response("There is not any user with the given email" , status=status.HTTP_404_NOT_FOUND)
        newCode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        try:
            u = VC_Codes.objects.get(email = email)
        except VC_Codes.DoesNotExist:
            return Response({'error': 'Invalid email'}, status=status.HTTP_401_UNAUTHORIZED)
        u.vc_code = newCode
        u.save()
        template = render_to_string('forgotpass_template.html',
            {'name': u.name,
                'code': newCode})
        data = {'to_email':u.email,'body':template, 'subject': 'NoWaste forgot password'}
        Util.send_email(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get(self, request):
        serializer = ForgotPasswordSerializer()
        return Response(serializer.data)

class ForgotPassVerify(APIView):
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        validate_email = EmailValidator()
        if serializer.is_valid():
            email =serializer.validated_data['email']
            try:
                validate_email.__call__(email)
            except ValidationError as e:
                return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = VC_Codes.objects.get(email=email)
            except VC_Codes.DoesNotExist:
                return Response("There is not any user with the given email" , status=status.HTTP_404_NOT_FOUND)
            if user.vc_code == serializer.validated_data['code']:
                new_serializer = MyAuthorSerializer()
                return Response(new_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("verification code is wrong", status=status.HTTP_400_BAD_REQUEST)
        return Response("error!", status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        serializer = EmailVerificationSerializer()
        return Response(serializer.data)

class ForgotPassSetNewPass(APIView):
    def post(self, request):
        serializer = MyAuthorSerializer(data=request.data)
        validate_email = EmailValidator()
        if serializer.is_valid(raise_exception=True):
            email =serializer.validated_data['email']
            try:
                validate_email.__call__(email)
            except ValidationError as e:
                return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = MyAuthor.objects.get(email=email)
            except MyAuthor.DoesNotExist:
                return Response("There is not any user with the given email" , status=status.HTTP_404_NOT_FOUND)
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("error!", status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        serializer = MyAuthorSerializer()
        return Response(serializer.data)

class ChangePasswordView(generics.UpdateAPIView):
    queryset = Customer.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def put(self, request, *args, **kwargs):
        user = request.user
        if(user.id != self.kwargs['pk']):
            return Response({"message": "Unathorized!"},status=status.HTTP_401_UNAUTHORIZED)
        super().update(request, *args, **kwargs) 
        return Response({"message" :"Password changed successfully!"},status= status.HTTP_200_OK)


class UpdateRetrieveProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Customer.objects.all()
    def get_queryset(self):
        return Customer.objects.filter(id=self.kwargs['id'])
    def get_serializer_class(self):
        if (self.request.method == 'GET'):
            return CustomerSerializer
        else :
            return UpdateUserSerializer
    lookup_field = 'id'
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    def get(self,request,id):
        if ( request.user.id != id ):
            return Response({"message": "Unathorized!"},status= status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
  

class CustomerProfileView(generics.RetrieveAPIView):  
    serializer_class = CustomerSerializer
    lookup_field = 'id'
    def get_queryset(self):
        return Customer.objects.filter(id=self.kwargs['id'])

    def get_serializer_context(self):
        return {'id': self.kwargs['id']}



class RateRestaurantView(APIView):
    def post(self, request):
        serializer = RateRestaurantSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data['name']
            try:
                restaurant = Restaurant.objects.get(name=name)
            except Restaurant.DoesNotExist:
                return Response("There is not any restaurant with the given name" , status=status.HTTP_404_NOT_FOUND)
            restaurant.rate = ((restaurant.rate)*restaurant.count_rates + serializer.validated_data['rate'])/(restaurant.count_rates+1)
            restaurant.count_rates += 1
            restaurant.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("error!", status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        serializer = RateRestaurantSerializer()
        return Response(serializer.data)