from decimal import Decimal
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import AnonymousUser
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
        fields = ['name', 'password', 'email', 'role']
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '*'

class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    class Meta:
        model = Customer
        fields = ['email']

class EmailVerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    code = serializers.CharField(max_length=6, required=True, allow_blank=False, allow_null=False)
    class Meta:
        model = Customer
        fields = ['email', 'code']


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True,source = 'password')

    class Meta:
        model = Customer
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    # def validate_old_password(self, value):
    #     user = self.context['request'].user
    #     if not user.check_password(value):
    #         raise serializers.ValidationError({"old_password": "Old password is not correct"})
    #     return value

    def validate_old_password(self, value):
        user = self.context['request'].user

        if isinstance(user, AnonymousUser):
            return value

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
        print(user.pk)
        print(instance.pk)
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    id = serializers.IntegerField()

    class Meta:
        model = Customer
        fields = ('username', 'name', 'email' ,'address','wallet_balance','gender','id')
        extra_kwargs = {
            'wallet_balance': {'read_only': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if Customer.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if Customer.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.name = validated_data['name']
        instance.username = validated_data['username']

        instance.save()

        return instance
    
