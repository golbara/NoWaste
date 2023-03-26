from decimal import Decimal
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ['password', 'email']

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'},
                                        required=True, allow_blank=False, allow_null=False,
                                        validators=[validate_password])
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'userName', 'password', 'email','phoneNumber']


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '*'

class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    class Meta:
        model = Customer
        fields = ['email']