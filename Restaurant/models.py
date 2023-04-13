<<<<<<< HEAD
from django.db import models
from django.core.validators import MinLengthValidator
=======
from django.db import models 
from django.core.validators import MinValueValidator,MinLengthValidator,RegexValidator
from django.contrib.auth.hashers import make_password
>>>>>>> 04aa06a8a5683214f1085c004d39860ef42526df

# Create your models here. 

<<<<<<< HEAD
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



    
=======
class Restaurant(models.Model): 

    name = models.CharField(max_length=255, unique=True) 
    address = models.CharField(max_length=255) 
    email = models.EmailField(max_length=255, unique=True) 
    discount = models.DecimalField(max_digits=2, decimal_places=2, blank=True, default=0) 
    purches_counts =models.IntegerField(blank= True, default=100) 
    password = models.CharField(max_length=8,validators=[MinLengthValidator(4)], null=True)
    def str(self) -> str: 
        return self.name 
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

class Food(models.Model): 
    name = models.CharField(max_length=255) 
    restaurants = models.ManyToManyField(Restaurant, related_name="food") 
    category = ( 
        ("drink", "Drink"),  
        ("iranian_food", "Iranian_food"),  
        ("foreign_food", "Foreign_food"),  
    ) 
    Type = models.CharField(choices=category,max_length=255) 
    def str(self) -> str: 
        return self.name 

class Food_Specifics(models.Model): 
    price = models.DecimalField(decimal_places=2,max_digits=20) 
    ingredients = models.CharField(max_length=1024, null=True) 
    FoodID = models.ForeignKey(Food, on_delete=models.CASCADE) 
    # Food_pic = models.ImageField(upload_to='Food_pics/', blank=True, null=True) 
    ResID = models.ForeignKey(Restaurant, on_delete=models.CASCADE) 
    class Meta: 
        unique_together = ('FoodID', 'ResID',)
>>>>>>> 04aa06a8a5683214f1085c004d39860ef42526df
