from django.db import models
from django.core.validators import MinValueValidator,MinLengthValidator,RegexValidator,MaxValueValidator
# from Restaurant.models import *
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
# from .managers import CustomUserManager,AuthorManager
from .managers import AuthorManager,RestaurantManager
from django.conf import settings
from datetime import *

class MyAuthor(AbstractBaseUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = AuthorManager()
    email = models.EmailField(unique= True)
    is_staff = models.BooleanField(default= False)
    is_active = models.BooleanField(default= True)
    is_superuser = models.BooleanField(default= False)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=16,validators=[MinLengthValidator(4)])
    role = models.CharField(max_length=255, default="customer")
    # For checking permissions. to keep it simple all admin have ALL permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

class RestaurantManager(MyAuthor):
    name = models.CharField(max_length=255, unique=True)
    manager_image = models.TextField(null= True , blank= True)
    number = models.CharField(max_length= 14,blank= True, null=True)
    def __str__(self) -> str:
        return self.name

class Restaurant(models.Model):
    address = models.CharField(max_length=255)
    name = models.CharField(max_length=255, unique=True)
    restaurant_image = models.TextField(null= True , blank= True)
    logo = models.TextField(null= True , blank= True)
    discount = models.DecimalField(max_digits=2, decimal_places=2,default=0.00)
    number = models.CharField(max_length= 14,blank= True, null=True)
    # this field is for when the number of purchases be more than a specific number , the discount would be given to the customer
    purches_counts =models.IntegerField(blank= True, default= 100)
    rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0.0,blank= True, null=True)
    count_rates = models.IntegerField(default=0,blank= True, null=True)
    date_of_establishment = models.DateField(default=date.today())
    description = models.CharField(max_length=1024 , default= "")
    manager = models.ForeignKey(RestaurantManager, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name

class Customer(MyAuthor):
    address = models.CharField(max_length=255 , default= "")
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True)
    customer_img = models.TextField(blank= True , null= True)
    phone_number = models.CharField(max_length=14,blank= True)
    gender_choice = (
        ("male", "Male"), 
        ("female", "Female"), 
    )
    gender = models.CharField(max_length=255,choices=gender_choice,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    wallet_balance = models.DecimalField(decimal_places=2, default=0,max_digits= 20,null= True)
    list_of_favorites_res = models.ManyToManyField(Restaurant, related_name='cust_favor_list', null= True , blank= True)
    def save(self, *args, **kwargs):
        self.username = self.name
        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.username
    

class VC_Codes(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique= True)
    vc_code = models.CharField(max_length=10, null=True)
    def __str__(self) -> str:
        return str(self.email)

