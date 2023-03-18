
from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import EmailValidator
from django.views.generic import View, UpdateView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import *
from .models import *
# from .tokens import account_activation_token
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string


class SignUpView(View):
    queryset = Customer.objects.all()
    serializer_class = CreateUserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if(serializer.is_valid(raise_exception=True)):
            self.save()
            headers = self.get_success_headers(serializer.data)
            # pk = serializer.instance.pk
            # self.verify_email(request, pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

