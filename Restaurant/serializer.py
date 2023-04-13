from decimal import Decimal
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import *

class RestaurantSerializer(serializers.ModelSerializer):
    def Menu(self):
        print("not implemented yet!")
    menu = serializers.SerializerMethodField(method_name= Menu)
    class Meta:
        model = Restaurant
        fields = ('name', 'email' ,'address','restaurant_image','menu')
        extra_kwargs = {
            'menu': {'read_only': True},
            'name' : {'required': False, 'allow_blank': True},
            'email' : {'required': False,'allow_null': True}
        }

    def validate_email(self, new_email):
        user = self.context['request'].user
        if Restaurant.objects.exclude(pk=user.pk).filter(email=new_email).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return new_email


    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
    


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True,source = 'password')

    class Meta:
        model = Restaurant
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        #  user = self.context['request'].user

        if not user.is_authenticated:
            raise serializers.ValidationError({"authorize": "You must be logged in to perform this action."})

        if user.pk != self.instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class FoodSerializer(serializers.ModelSerializer):
    class Meata :
        model = Food
        fields = ['__all__']