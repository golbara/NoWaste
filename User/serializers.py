from decimal import Decimal
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import *

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'},
                                        required=True, allow_blank=False, allow_null=False,
                                        validators=[validate_password])
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'username', 'password', 'email']

    def create(self, validated_data):
        new_user = Customer.objects.create_user(**validated_data)
        new_user.set_password(validated_data['password'])
        return new_user