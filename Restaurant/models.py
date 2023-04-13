from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    restaurant_image = models.ImageField(null= True , blank= True)
    email = models.EmailField(max_length=255, unique=True)
    discount = models.DecimalField(max_digits=2, decimal_places=2, blank=True)

    # this field is for when the number of purchases be more than a specific number , the discount would be given to the customer
    purches_counts =models.IntegerField(blank= True)
    password = models.CharField(max_length=8,validators=[MinLengthValidator(4)])
    email_confirmed = models.BooleanField(default=False)
    vc_code = models.CharField(max_length=6, null=True)
    def __str__(self) -> str:
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=255)
    food_image = models.ImageField(null= True, blank= True)
    category = (
        ("drink", "Drink"), 
        ("iranian_food", "Iranian_food"), 
        ("foreign_food", "Foreign_food"), 
    )
    price = models.DecimalField(decimal_places=2,max_digits=20 , null= True )
    ingredients = models.CharField(max_length=2048, null=True , blank=True)
    Food_pic = models.ImageField(upload_to='Food_pics/', blank=True, null=True)
    Type = models.CharField(choices=category,max_length=255, blank=True)
    def __str__(self) -> str:
        return self.name



    