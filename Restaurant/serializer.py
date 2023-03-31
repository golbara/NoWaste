from decimal import Decimal
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import *

class RestaurantSerializer(serializers.ModelSerializer):

    def Menu(self):
        print("not implemented yet!")
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'username', 'password', 'email']
    menu = serializers.SerializerMethodField(method_name= Menu)
