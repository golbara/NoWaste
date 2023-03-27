
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
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate, logout
from .authentication import create_access_token
import jwt,json

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
        try :
            user = Customer.objects.get( email = email , password = password)
            print(user)
        except not user :
            print(":)")
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        payload = { 'password':password,'email':email}
        jwt_token = {'token':jwt.encode(payload,"SECRET_kEY")}
        print(f'access_token:{jwt_token}')
        response = Response()
        response.set_cookie(key= 'jwt_token',value= jwt_token['token'],httponly= True)
        response.data =jwt_token
        return response
    def get(self,request):
        serializer = LoginSerializer()
        return Response(serializer.data)

@permission_classes((IsAuthenticated,))
class LogoutView(APIView):
    # This function delete token from database
    def delete_token(self ,token):
        try:
            token_obj = Token.objects.get(token=token)
            token_obj.delete()
        except :
            pass
    def get(self, request):
        response = Response()
        token = request.COOKIES.get('jwt_token')
        # delete token from database
        self.delete_token(token)
        # delete cookie
        response.delete_cookie(key='jwt_token')
        print(response.cookies)
        return Response({'message':"User successfully logged out."}, status=status.HTTP_200_OK)




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
