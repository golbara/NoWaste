from django.db import models
from django.core.validators import MinValueValidator,MinLengthValidator,RegexValidator
from Restaurant.models import *
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import CustomUserManager
class Customer(AbstractBaseUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    # objects = CustomUserManager
    role = models.CharField(max_length=255, default="Customer")
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    Name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    userName = models.CharField(max_length=255, default=Name
                                )
    email = models.EmailField(unique= True)
    email_confirmed = models.BooleanField(default=False)
    phoneNumber = models.CharField(max_length=11,validators=[RegexValidator(regex='^09\d{9}$', 
                                                       message='Phone number must be entered in the format: "09123456789". Up to 15 digits allowed.')])
    gender_CHoice = (
        ("male", "Male"), 
        ("female", "Female"), 
    )
    gender = models.CharField(max_length=255,choices=gender_CHoice,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    password = models.CharField(max_length=8,validators=[MinLengthValidator(4)])
    wallet_balance = models.DecimalField(decimal_places=2, default=0,max_digits= 20,null= True)
    list_of_favorites_res = models.ManyToManyField(Restaurant, related_name='cust_favor_list')

    def __str__(self) -> str:
        return self.userName
    